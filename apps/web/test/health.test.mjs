import assert from "node:assert/strict";
import test from "node:test";

import { parseApiReadiness, readinessUrl } from "../dist/health.js";

const checkedAt = "2026-07-19T12:00:00Z";
const payload = {
  service: "api",
  checked_at: checkedAt,
  status: "degraded",
  dependencies: {
    postgres: { status: "ready", checked_at: checkedAt },
    redis: {
      status: "unavailable",
      checked_at: checkedAt,
      detail: "connection refused",
    },
  },
  capabilities: {
    read_only_api: { status: "degraded" },
    background_jobs: { status: "unready" },
  },
};

test("parses the documented degraded readiness payload", () => {
  assert.deepEqual(parseApiReadiness(payload), {
    service: "api",
    checkedAt,
    status: "degraded",
    dependencies: {
      postgres: { status: "ready", checkedAt },
      redis: { status: "unavailable", checkedAt, detail: "connection refused" },
    },
    capabilities: { readOnlyApi: "degraded", backgroundJobs: "unready" },
  });
});

test("rejects malformed readiness data rather than presenting it as ready", () => {
  assert.equal(
    parseApiReadiness({ ...payload, checked_at: "not a timestamp" }),
    undefined,
  );
  assert.equal(
    parseApiReadiness({
      ...payload,
      capabilities: { read_only_api: { status: "ready" } },
    }),
    undefined,
  );
});

test("uses the readiness route and normalizes a trailing slash", () => {
  assert.equal(
    readinessUrl("http://localhost:8000/"),
    "http://localhost:8000/health/ready",
  );
});
