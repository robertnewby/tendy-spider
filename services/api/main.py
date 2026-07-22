"""HTTP entrypoint for the Tendy Spider API service."""

from __future__ import annotations

import os
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Literal
from urllib.parse import urlsplit

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, field_validator

from .health import (
    DependencyCheck,
    DependencyProbe,
    DependencyStatus,
    HealthService,
    HealthStatus,
    TcpDependencyProbe,
    utc_now,
)

LOCAL_DEVELOPMENT_ORIGINS = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
)


class OperationalModel(BaseModel):
    """Strict operational metadata with a UTC-only internal representation."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class LivenessResponse(OperationalModel):
    service: Literal["api"] = "api"
    checked_at: datetime
    status: Literal["live"] = "live"

    @field_validator("checked_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("checked_at must include a UTC offset")
        return value.astimezone(UTC)


class DependencyResponse(OperationalModel):
    status: DependencyStatus
    checked_at: datetime
    detail: str | None = None

    @field_validator("checked_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("checked_at must include a UTC offset")
        return value.astimezone(UTC)


class CapabilityResponse(OperationalModel):
    status: HealthStatus


class CapabilitiesResponse(OperationalModel):
    read_only_api: CapabilityResponse
    background_jobs: CapabilityResponse


class ReadinessResponse(OperationalModel):
    service: Literal["api"] = "api"
    checked_at: datetime
    status: HealthStatus
    dependencies: dict[Literal["postgres", "redis"], DependencyResponse]
    capabilities: CapabilitiesResponse

    @field_validator("checked_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("checked_at must include a UTC offset")
        return value.astimezone(UTC)


def _dependency_response(check: DependencyCheck) -> DependencyResponse:
    return DependencyResponse(
        status=check.status,
        checked_at=check.checked_at,
        detail=check.detail,
    )


def _default_probes() -> dict[str, DependencyProbe]:
    """Build local adapters from environment without loading provider SDKs."""

    return {
        "postgres": TcpDependencyProbe(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
        ),
        "redis": TcpDependencyProbe(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", "6379")),
        ),
    }


def _validate_cors_origins(origins: Sequence[str]) -> tuple[str, ...]:
    """Reject wildcard and non-origin CORS settings before the API starts."""

    validated: list[str] = []
    for origin in origins:
        candidate = origin.strip()
        parsed = urlsplit(candidate)
        if (
            not candidate
            or "*" in candidate
            or parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or parsed.path
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(f"invalid API CORS origin: {origin!r}")
        if candidate not in validated:
            validated.append(candidate)
    return tuple(validated)


def _cors_origins_from_environment() -> tuple[str, ...]:
    """Read a comma-delimited allowlist, defaulting only to local web origins."""

    configured_origins = os.getenv("API_CORS_ORIGINS")
    if configured_origins is None:
        return LOCAL_DEVELOPMENT_ORIGINS
    return _validate_cors_origins(configured_origins.split(","))


def create_app(
    probes: dict[str, DependencyProbe] | None = None,
    cors_origins: Sequence[str] | None = None,
) -> FastAPI:
    """Construct the API with injectable dependency probes for offline tests."""

    health_service = HealthService(probes if probes is not None else _default_probes())
    app = FastAPI(title="Tendy Spider API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(
            _validate_cors_origins(cors_origins)
            if cors_origins is not None
            else _cors_origins_from_environment()
        ),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=[],
    )

    @app.get("/health/live", response_model=LivenessResponse)
    async def live() -> LivenessResponse:
        """Report process liveness without checking Postgres or Redis."""

        return LivenessResponse(checked_at=utc_now())

    async def readiness_response(response: Response) -> ReadinessResponse:
        readiness = await health_service.readiness()
        if readiness.status is HealthStatus.UNREADY:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadinessResponse(
            checked_at=utc_now(),
            status=readiness.status,
            dependencies={
                "postgres": _dependency_response(readiness.postgres),
                "redis": _dependency_response(readiness.redis),
            },
            capabilities=CapabilitiesResponse(
                read_only_api=CapabilityResponse(status=readiness.read_only_api_status),
                background_jobs=CapabilityResponse(status=readiness.background_jobs_status),
            ),
        )

    app.add_api_route(
        "/health/ready",
        readiness_response,
        methods=["GET"],
        response_model=ReadinessResponse,
    )
    app.add_api_route(
        "/health",
        readiness_response,
        methods=["GET"],
        response_model=ReadinessResponse,
    )
    return app


app = create_app()
