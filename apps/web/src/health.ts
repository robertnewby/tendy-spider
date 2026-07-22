export type ReadinessStatus = "ready" | "degraded" | "unready";
export type DependencyStatus = "ready" | "unavailable";
export type BackgroundJobStatus = "ready" | "unready";

export interface ApiReadiness {
  service: "api";
  checkedAt: string;
  status: ReadinessStatus;
  dependencies: {
    postgres: DependencyReadiness;
    redis: DependencyReadiness;
  };
  capabilities: {
    readOnlyApi: ReadinessStatus;
    backgroundJobs: BackgroundJobStatus;
  };
}

export interface DependencyReadiness {
  status: DependencyStatus;
  checkedAt: string;
  detail?: string;
}

type JsonRecord = Record<string, unknown>;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isTimestamp(value: unknown): value is string {
  return typeof value === "string" && !Number.isNaN(Date.parse(value));
}

function dependency(value: unknown): DependencyReadiness | undefined {
  if (!isRecord(value)) return undefined;
  if (
    (value.status !== "ready" && value.status !== "unavailable") ||
    !isTimestamp(value.checked_at)
  ) {
    return undefined;
  }
  if (value.detail !== undefined && typeof value.detail !== "string") {
    return undefined;
  }
  return {
    status: value.status,
    checkedAt: value.checked_at,
    ...(typeof value.detail === "string" ? { detail: value.detail } : {}),
  };
}

export function parseApiReadiness(payload: unknown): ApiReadiness | undefined {
  if (
    !isRecord(payload) ||
    payload.service !== "api" ||
    !isTimestamp(payload.checked_at)
  ) {
    return undefined;
  }
  if (
    payload.status !== "ready" &&
    payload.status !== "degraded" &&
    payload.status !== "unready"
  ) {
    return undefined;
  }
  if (!isRecord(payload.dependencies) || !isRecord(payload.capabilities)) {
    return undefined;
  }

  const postgres = dependency(payload.dependencies.postgres);
  const redis = dependency(payload.dependencies.redis);
  const { read_only_api: readOnlyApi, background_jobs: backgroundJobs } =
    payload.capabilities;

  if (
    !postgres ||
    !redis ||
    !isRecord(readOnlyApi) ||
    !isRecord(backgroundJobs) ||
    (readOnlyApi.status !== "ready" &&
      readOnlyApi.status !== "degraded" &&
      readOnlyApi.status !== "unready") ||
    (backgroundJobs.status !== "ready" && backgroundJobs.status !== "unready")
  ) {
    return undefined;
  }

  return {
    service: "api",
    checkedAt: payload.checked_at,
    status: payload.status,
    dependencies: { postgres, redis },
    capabilities: {
      readOnlyApi: readOnlyApi.status,
      backgroundJobs: backgroundJobs.status,
    },
  };
}

export function readinessUrl(apiBaseUrl: string): string {
  return `${apiBaseUrl.replace(/\/$/, "")}/health/ready`;
}
