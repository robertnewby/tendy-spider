"""Pydantic enforcement for the canonical JSON Schemas.

JSON Schema is the portable source of truth. These models intentionally add
cross-field validation for semantics that are awkward or impossible to state
portably in JSON Schema.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    AnyUrl,
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    field_validator,
    model_validator,
)

ContractVersion = Literal["1.0.0"]
CONTRACT_VERSION: ContractVersion = "1.0.0"
NonEmpty = Annotated[str, Field(min_length=1)]
NonNegativeDecimal = Annotated[Decimal, Field(ge=0)]
PositiveDecimal = Annotated[Decimal, Field(gt=0)]
FactValue = Annotated[Decimal | str | bool, Field(union_mode="left_to_right")]
MacroValue = Annotated[Decimal | str, Field(union_mode="left_to_right")]


def _as_utc(value: datetime | None, field_description: str) -> datetime | None:
    if value is not None and (value.tzinfo is None or value.utcoffset() is None):
        raise ValueError(f"{field_description} must include a UTC offset")
    return value.astimezone(UTC) if value is not None else None


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceIdentity(StrictModel):
    publisher: NonEmpty
    source_record_id: NonEmpty | None = None
    source_url: AnyUrl | None = None
    dataset: NonEmpty | None = None

    @model_validator(mode="after")
    def require_identifier(self) -> SourceIdentity:
        if self.source_record_id is None and self.source_url is None:
            raise ValueError("source_record_id or source_url is required")
        return self


class ObservationTimes(StrictModel):
    observed_at: datetime
    knowable_at: datetime
    retrieved_at: datetime
    expires_at: datetime | None = None

    @field_validator("*")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "timestamps")

    @model_validator(mode="after")
    def validate_order(self) -> ObservationTimes:
        if self.knowable_at > self.retrieved_at:
            raise ValueError("knowable_at must not be after retrieved_at")
        if self.expires_at is not None and self.expires_at < self.knowable_at:
            raise ValueError("expires_at must not be before knowable_at")
        return self


class Freshness(StrictModel):
    status: Literal["fresh", "stale", "expired", "unknown"]
    determined_at: datetime
    max_age_seconds: Annotated[int, Field(ge=0)] | None = None
    latency_seconds: Annotated[int, Field(ge=0)] | None = None
    reason: NonEmpty | None = None

    @field_validator("determined_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "determined_at")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def explain_nonfresh(self) -> Freshness:
        if self.status in {"stale", "expired", "unknown"} and self.reason is None:
            raise ValueError("non-fresh observations require a reason")
        return self


class SessionMetadata(StrictModel):
    venue_id: NonEmpty | None = None
    session: Literal["pre_market", "regular", "after_hours", "overnight", "continuous", "unknown"]
    source_timezone: NonEmpty

    @field_validator("source_timezone")
    @classmethod
    def require_iana_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("source_timezone must be an IANA timezone name") from exc
        return value


class AdjustmentMode(str, Enum):
    NONE = "none"
    SPLIT = "split"
    SPLIT_DIVIDEND = "split_dividend"
    PROVIDER_DEFINED = "provider_defined"


class Adjustment(StrictModel):
    mode: AdjustmentMode
    methodology: NonEmpty | None = None
    adjustment_as_of: datetime | None = None

    @field_validator("adjustment_as_of")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "adjustment_as_of")

    @model_validator(mode="after")
    def explain_provider_adjustment(self) -> Adjustment:
        if self.mode is AdjustmentMode.PROVIDER_DEFINED and self.methodology is None:
            raise ValueError("provider_defined adjustment requires methodology")
        return self


class UsagePolicy(StrictModel):
    display: Literal["allowed", "attribution_required", "prohibited", "unknown"]
    storage: Literal["permanent", "time_limited", "transient", "prohibited", "unknown"]
    retention_days: Annotated[int, Field(ge=0)] | None = None
    redistribution: Literal["allowed", "derived_only", "prohibited", "unknown"]
    attribution_text: NonEmpty | None = None
    model_training_allowed: bool | None = None
    terms_url: AnyUrl | None = None
    policy_as_of: datetime

    @field_validator("policy_as_of")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "policy_as_of")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_policy(self) -> UsagePolicy:
        if self.storage == "time_limited" and self.retention_days is None:
            raise ValueError("time_limited storage requires retention_days")
        if self.display == "attribution_required" and self.attribution_text is None:
            raise ValueError("attribution_required display requires attribution_text")
        return self


class Transformation(StrictModel):
    name: NonEmpty
    code_version: NonEmpty
    data_version: NonEmpty
    parameters: dict[str, Any] = Field(default_factory=dict)


class Lineage(StrictModel):
    stage: Literal["raw", "normalized", "derived"]
    record_id: NonEmpty
    parent_record_ids: list[NonEmpty] = Field(default_factory=list)
    transformation: Transformation | None = None

    @model_validator(mode="after")
    def validate_stage(self) -> Lineage:
        if self.stage == "raw":
            if self.parent_record_ids or self.transformation is not None:
                raise ValueError("raw records cannot declare parents or transformations")
        elif not self.parent_record_ids or self.transformation is None:
            raise ValueError("normalized and derived records require parents and transformation")
        return self


class Provenance(StrictModel):
    source: SourceIdentity
    times: ObservationTimes
    freshness: Freshness
    policy: UsagePolicy
    lineage: Lineage

    @model_validator(mode="after")
    def validate_freshness_against_expiration(self) -> Provenance:
        expires_at = self.times.expires_at
        if (
            expires_at is not None
            and self.freshness.determined_at >= expires_at
            and self.freshness.status == "fresh"
        ):
            raise ValueError("an observation cannot be fresh at or after expires_at")
        if self.freshness.status == "expired" and (
            expires_at is None or self.freshness.determined_at < expires_at
        ):
            raise ValueError("expired status requires a reached expires_at")
        return self


class ContractRecord(StrictModel):
    contract_version: ContractVersion = CONTRACT_VERSION
    provenance: Provenance


class InstrumentIdentity(ContractRecord):
    contract_type: Literal["instrument_identity"]
    instrument_id: NonEmpty
    asset_class: Literal["equity", "etf", "index", "crypto", "fx", "future", "option", "macro"]
    name: NonEmpty
    issuer_id: NonEmpty | None = None
    primary_venue_id: NonEmpty | None = None
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")] | None = None
    active_from: datetime
    active_to: datetime | None = None

    @field_validator("active_from", "active_to")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "identity bounds")

    @model_validator(mode="after")
    def validate_active_range(self) -> InstrumentIdentity:
        if self.active_to is not None and self.active_to <= self.active_from:
            raise ValueError("active_to must be after active_from")
        return self


class SymbolMapping(ContractRecord):
    contract_type: Literal["symbol_mapping"]
    instrument_id: NonEmpty
    symbol: NonEmpty
    venue_id: NonEmpty
    valid_from: datetime
    valid_to: datetime | None = None
    mapping_status: Literal["active", "renamed", "delisted", "historical"]
    predecessor_symbol: NonEmpty | None = None

    @field_validator("valid_from", "valid_to")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "symbol bounds")

    @model_validator(mode="after")
    def validate_mapping(self) -> SymbolMapping:
        if self.valid_to is not None and self.valid_to <= self.valid_from:
            raise ValueError("valid_to must be after valid_from")
        if self.mapping_status == "renamed" and self.predecessor_symbol is None:
            raise ValueError("renamed mappings require predecessor_symbol")
        return self


class PriceBar(ContractRecord):
    contract_type: Literal["price_bar"]
    instrument_id: NonEmpty
    bar_start: datetime
    bar_end: datetime
    interval: NonEmpty
    session: SessionMetadata
    unit: Literal["price"]
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")]
    adjustment: Adjustment
    open: PositiveDecimal
    high: PositiveDecimal
    low: PositiveDecimal
    close: PositiveDecimal
    volume: NonNegativeDecimal | None = None

    @field_validator("bar_start", "bar_end")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "bar timestamps")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_bar(self) -> PriceBar:
        if self.bar_end <= self.bar_start:
            raise ValueError("bar_end must be after bar_start")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must be the greatest OHLC value")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be the least OHLC value")
        return self


class Quote(ContractRecord):
    contract_type: Literal["quote"]
    instrument_id: NonEmpty
    quoted_at: datetime
    session: SessionMetadata
    unit: Literal["price"]
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")]
    bid_price: PositiveDecimal | None = None
    bid_size: NonNegativeDecimal | None = None
    ask_price: PositiveDecimal | None = None
    ask_size: NonNegativeDecimal | None = None

    @field_validator("quoted_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "quoted_at")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_quote(self) -> Quote:
        if self.bid_price is None and self.ask_price is None:
            raise ValueError("at least one quote side is required")
        if (
            self.bid_price is not None
            and self.ask_price is not None
            and self.bid_price > self.ask_price
        ):
            raise ValueError("bid_price must not exceed ask_price")
        if (self.bid_price is None) != (self.bid_size is None):
            raise ValueError("bid price and size must be supplied together")
        if (self.ask_price is None) != (self.ask_size is None):
            raise ValueError("ask price and size must be supplied together")
        return self


class Period(StrictModel):
    start: datetime
    end: datetime
    fiscal_year: int | None = None
    fiscal_period: NonEmpty | None = None

    @field_validator("start", "end")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "period bounds")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_period(self) -> Period:
        if self.end < self.start:
            raise ValueError("period end must not be before start")
        return self


class FundamentalFact(ContractRecord):
    contract_type: Literal["fundamental_fact"]
    instrument_id: NonEmpty
    concept: NonEmpty
    value: FactValue
    unit: NonEmpty
    period: Period
    form: NonEmpty
    filing_id: NonEmpty
    fact_status: Literal["preliminary", "reported", "restated"]
    supersedes_record_id: NonEmpty | None = None

    @model_validator(mode="after")
    def validate_restatement(self) -> FundamentalFact:
        if self.fact_status == "restated" and self.supersedes_record_id is None:
            raise ValueError("restated facts require supersedes_record_id")
        if self.fact_status != "restated" and self.supersedes_record_id is not None:
            raise ValueError("only restated facts may supersede another fact")
        return self


class Filing(ContractRecord):
    contract_type: Literal["filing"]
    instrument_id: NonEmpty
    filing_id: NonEmpty
    form: NonEmpty
    filed_at: datetime
    period_end: datetime | None = None
    amendment: bool
    amends_filing_id: NonEmpty | None = None
    document_url: AnyUrl

    @field_validator("filed_at", "period_end")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "filing timestamps")

    @model_validator(mode="after")
    def validate_amendment(self) -> Filing:
        if self.amendment != (self.amends_filing_id is not None):
            raise ValueError("amendment and amends_filing_id must agree")
        return self


class CorporateAction(ContractRecord):
    contract_type: Literal["corporate_action"]
    instrument_id: NonEmpty
    action_type: Literal[
        "split", "reverse_split", "cash_dividend", "stock_dividend", "rename", "merger", "spinoff"
    ]
    effective_at: datetime
    ratio_numerator: PositiveDecimal | None = None
    ratio_denominator: PositiveDecimal | None = None
    cash_amount: NonNegativeDecimal | None = None
    currency: Annotated[str, Field(pattern=r"^[A-Z]{3}$")] | None = None

    @field_validator("effective_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "effective_at")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_action(self) -> CorporateAction:
        is_split = self.action_type in {"split", "reverse_split", "stock_dividend"}
        if is_split and (self.ratio_numerator is None or self.ratio_denominator is None):
            raise ValueError("split-like actions require a ratio")
        if self.action_type == "cash_dividend" and (
            self.cash_amount is None or self.currency is None
        ):
            raise ValueError("cash dividends require cash_amount and currency")
        return self


class MacroObservation(ContractRecord):
    contract_type: Literal["macro_observation"]
    series_id: NonEmpty
    period: Period
    value: MacroValue
    unit: NonEmpty
    frequency: NonEmpty
    vintage_date: datetime
    observation_status: Literal["preliminary", "revised", "final"]
    supersedes_record_id: NonEmpty | None = None

    @field_validator("vintage_date")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        converted = _as_utc(value, "vintage_date")
        assert converted is not None
        return converted

    @model_validator(mode="after")
    def validate_revision(self) -> MacroObservation:
        if self.observation_status == "revised" and self.supersedes_record_id is None:
            raise ValueError("revised macro values require supersedes_record_id")
        return self


class Document(ContractRecord):
    contract_type: Literal["document"]
    document_id: NonEmpty
    document_kind: Literal["filing", "news", "press_release", "transcript", "research", "other"]
    title: NonEmpty
    published_at: datetime
    updated_at: datetime | None = None
    language: Annotated[str, Field(pattern=r"^[a-z]{2,3}(-[A-Z]{2})?$")]
    canonical_url: AnyUrl
    instrument_ids: list[NonEmpty] = Field(default_factory=list)
    content_hash: Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")] | None = None
    full_text_storage: Literal["stored", "metadata_only", "prohibited"]

    @field_validator("published_at", "updated_at")
    @classmethod
    def require_timezone(cls, value: datetime | None) -> datetime | None:
        return _as_utc(value, "document timestamps")

    @model_validator(mode="after")
    def validate_update(self) -> Document:
        if self.updated_at is not None and self.updated_at < self.published_at:
            raise ValueError("updated_at must not precede published_at")
        if self.full_text_storage == "stored" and self.content_hash is None:
            raise ValueError("stored documents require content_hash")
        return self


class EvidenceItem(ContractRecord):
    contract_type: Literal["evidence_item"]
    evidence_id: NonEmpty
    claim: NonEmpty
    support_type: Literal["direct", "derived", "contradictory", "context"]
    source_record_ids: Annotated[list[NonEmpty], Field(min_length=1)]
    excerpt: NonEmpty | None = None
    locator: NonEmpty | None = None
    confidence: Annotated[Decimal, Field(ge=0, le=1)]

    @model_validator(mode="after")
    def validate_derived_support(self) -> EvidenceItem:
        if self.support_type == "derived" and self.provenance.lineage.stage != "derived":
            raise ValueError("derived evidence requires derived lineage")
        return self


class MarketStatistic(ContractRecord):
    contract_type: Literal["market_statistic"]
    instrument_id: NonEmpty
    metric_kind: Literal["short_volume", "short_interest", "ats_volume", "other"]
    period: Period
    venue_id: NonEmpty | None = None
    value: NonNegativeDecimal
    unit: NonEmpty
    publication_cadence: NonEmpty


Contract = (
    InstrumentIdentity
    | SymbolMapping
    | PriceBar
    | Quote
    | FundamentalFact
    | Filing
    | CorporateAction
    | MacroObservation
    | Document
    | EvidenceItem
    | MarketStatistic
)

_CONTRACT_ADAPTER: TypeAdapter[Contract] = TypeAdapter(
    Annotated[Contract, Field(discriminator="contract_type")]
)


def validate_contract(data: dict[str, Any]) -> Contract:
    """Validate an untrusted contract payload and return its typed representation."""

    return _CONTRACT_ADAPTER.validate_python(data)
