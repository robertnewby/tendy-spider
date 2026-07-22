"""Offline health policy tests for the API boundary."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from services.api.health import DependencyCheck, DependencyStatus
from services.api.main import LOCAL_DEVELOPMENT_ORIGINS, create_app

CHECKED_AT = datetime(2026, 7, 19, 18, 0, tzinfo=UTC)


class RecordingProbe:
    def __init__(self, result: DependencyCheck) -> None:
        self.result = result
        self.calls = 0

    async def check(self) -> DependencyCheck:
        self.calls += 1
        return self.result


def probe(status: DependencyStatus, detail: str | None = None) -> RecordingProbe:
    return RecordingProbe(DependencyCheck(status=status, checked_at=CHECKED_AT, detail=detail))


def test_liveness_is_process_only() -> None:
    postgres = probe(DependencyStatus.UNAVAILABLE, "fixture postgres outage")
    redis = probe(DependencyStatus.UNAVAILABLE, "fixture redis outage")

    response = TestClient(create_app({"postgres": postgres, "redis": redis})).get("/health/live")

    assert response.status_code == 200
    assert response.json()["service"] == "api"
    assert response.json()["status"] == "live"
    assert response.json()["checked_at"].endswith("Z") or response.json()["checked_at"].endswith(
        "+00:00"
    )
    assert postgres.calls == 0
    assert redis.calls == 0


def test_readiness_is_ready_when_postgres_and_redis_are_available() -> None:
    postgres = probe(DependencyStatus.READY)
    redis = probe(DependencyStatus.READY)

    response = TestClient(create_app({"postgres": postgres, "redis": redis})).get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "service": "api",
        "checked_at": response.json()["checked_at"],
        "status": "ready",
        "dependencies": {
            "postgres": {
                "status": "ready",
                "checked_at": "2026-07-19T18:00:00Z",
                "detail": None,
            },
            "redis": {
                "status": "ready",
                "checked_at": "2026-07-19T18:00:00Z",
                "detail": None,
            },
        },
        "capabilities": {
            "read_only_api": {"status": "ready"},
            "background_jobs": {"status": "ready"},
        },
    }


def test_postgres_outage_makes_the_api_unready() -> None:
    postgres = probe(DependencyStatus.UNAVAILABLE, "fixture postgres outage")
    redis = probe(DependencyStatus.READY)

    response = TestClient(create_app({"postgres": postgres, "redis": redis})).get("/health")

    assert response.status_code == 503
    assert response.json()["status"] == "unready"
    assert response.json()["dependencies"]["postgres"]["status"] == "unavailable"
    assert response.json()["capabilities"] == {
        "read_only_api": {"status": "unready"},
        "background_jobs": {"status": "unready"},
    }


def test_redis_outage_degrades_read_only_api_and_stops_background_jobs() -> None:
    postgres = probe(DependencyStatus.READY)
    redis = probe(DependencyStatus.UNAVAILABLE, "fixture redis outage")
    client = TestClient(create_app({"postgres": postgres, "redis": redis}))

    ready_response = client.get("/health/ready")
    alias_response = client.get("/health")

    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "degraded"
    assert ready_response.json()["capabilities"] == {
        "read_only_api": {"status": "degraded"},
        "background_jobs": {"status": "unready"},
    }
    assert alias_response.status_code == 200
    assert alias_response.json()["status"] == "degraded"


def test_local_web_origin_is_allowed_for_get_preflight() -> None:
    client = TestClient(create_app(cors_origins=LOCAL_DEVELOPMENT_ORIGINS))

    response = client.options(
        "/health/live",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
    assert response.headers["access-control-allow-methods"] == "GET"
    assert "access-control-allow-credentials" not in response.headers


def test_disallowed_cors_origin_is_not_granted_preflight_access() -> None:
    client = TestClient(create_app(cors_origins=LOCAL_DEVELOPMENT_ORIGINS))

    response = client.options(
        "/health/live",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_cors_origins_can_be_configured_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_CORS_ORIGINS", "http://localhost:3000")
    client = TestClient(create_app())

    response = client.options(
        "/health/live",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_configuration_rejects_wildcards() -> None:
    with pytest.raises(ValueError, match="invalid API CORS origin"):
        create_app(cors_origins=["*"])
