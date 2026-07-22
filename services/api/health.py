"""Dependency readiness policy for the API process.

The probe protocol keeps this operational boundary independent of a particular
database or queue SDK. Production wiring may use a real client behind the
protocol; unit tests use static fakes and never connect to a network service.
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol


def utc_now() -> datetime:
    """Return an aware UTC timestamp for operational responses."""

    return datetime.now(UTC)


class DependencyStatus(StrEnum):
    READY = "ready"
    UNAVAILABLE = "unavailable"


class HealthStatus(StrEnum):
    READY = "ready"
    DEGRADED = "degraded"
    UNREADY = "unready"


@dataclass(frozen=True, slots=True)
class DependencyCheck:
    """A point-in-time dependency probe result with no provider-specific type."""

    status: DependencyStatus
    checked_at: datetime
    detail: str | None = None

    def __post_init__(self) -> None:
        if self.checked_at.tzinfo is None or self.checked_at.utcoffset() is None:
            raise ValueError("dependency check timestamps must include a UTC offset")
        object.__setattr__(self, "checked_at", self.checked_at.astimezone(UTC))


class DependencyProbe(Protocol):
    """Minimal adapter boundary for an API dependency readiness check."""

    async def check(self) -> DependencyCheck:
        """Return a current status; callers turn failures into explicit health state."""


@dataclass(frozen=True, slots=True)
class StaticDependencyProbe:
    """Offline fixture adapter for deterministic tests and local diagnostics."""

    result: DependencyCheck

    async def check(self) -> DependencyCheck:
        return self.result


@dataclass(frozen=True, slots=True)
class TcpDependencyProbe:
    """A lightweight adapter that tests whether a local dependency accepts TCP.

    It is intentionally not a database or Redis SDK. Authentication and
    provider-specific commands belong to future explicit adapters.
    """

    host: str
    port: int
    timeout_seconds: float = 1.0

    async def check(self) -> DependencyCheck:
        checked_at = utc_now()
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout=self.timeout_seconds
            )
            del reader
            writer.close()
            await writer.wait_closed()
        except (OSError, TimeoutError) as exc:
            return DependencyCheck(
                status=DependencyStatus.UNAVAILABLE,
                checked_at=checked_at,
                detail=type(exc).__name__,
            )
        return DependencyCheck(status=DependencyStatus.READY, checked_at=checked_at)


@dataclass(frozen=True, slots=True)
class ReadinessResult:
    """Derived capability state from independently measured dependencies."""

    status: HealthStatus
    postgres: DependencyCheck
    redis: DependencyCheck

    @property
    def read_only_api_status(self) -> HealthStatus:
        if self.postgres.status is DependencyStatus.UNAVAILABLE:
            return HealthStatus.UNREADY
        if self.redis.status is DependencyStatus.UNAVAILABLE:
            return HealthStatus.DEGRADED
        return HealthStatus.READY

    @property
    def background_jobs_status(self) -> HealthStatus:
        if (
            self.postgres.status is DependencyStatus.UNAVAILABLE
            or self.redis.status is DependencyStatus.UNAVAILABLE
        ):
            return HealthStatus.UNREADY
        return HealthStatus.READY


class HealthService:
    """Applies the documented readiness policy over injected dependency probes."""

    def __init__(self, probes: Mapping[str, DependencyProbe]) -> None:
        required = {"postgres", "redis"}
        if set(probes) != required:
            raise ValueError("health probes must contain exactly postgres and redis")
        self._probes = dict(probes)

    async def readiness(self) -> ReadinessResult:
        postgres, redis = await asyncio.gather(
            self._probe("postgres"),
            self._probe("redis"),
        )
        if postgres.status is DependencyStatus.UNAVAILABLE:
            status = HealthStatus.UNREADY
        elif redis.status is DependencyStatus.UNAVAILABLE:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.READY
        return ReadinessResult(status=status, postgres=postgres, redis=redis)

    async def _probe(self, name: str) -> DependencyCheck:
        try:
            return await self._probes[name].check()
        except Exception as exc:  # pragma: no cover - defensive adapter boundary
            return DependencyCheck(
                status=DependencyStatus.UNAVAILABLE,
                checked_at=utc_now(),
                detail=type(exc).__name__,
            )
