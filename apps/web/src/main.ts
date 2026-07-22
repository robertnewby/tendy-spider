import {
  parseApiReadiness,
  readinessUrl,
  type ApiReadiness,
} from "./health.js";

type WorkspaceState =
  | { kind: "loading" }
  | { kind: "connection-error"; message: string }
  | { kind: "invalid-response" }
  | { kind: "ready" | "degraded" | "unready"; readiness: ApiReadiness };

declare global {
  interface Window {
    TENDY_SPIDER_CONFIG?: { apiBaseUrl?: string };
  }
}

const app = document.querySelector<HTMLElement>("#app");
const baseUrlMeta = document.querySelector<HTMLMetaElement>(
  'meta[name="tendy-api-base-url"]',
);
const apiBaseUrl =
  window.TENDY_SPIDER_CONFIG?.apiBaseUrl ??
  baseUrlMeta?.content ??
  "http://localhost:8000";

if (!app) {
  throw new Error("Research workspace root is missing.");
}
const appElement: HTMLElement = app;

function statusLabel(state: WorkspaceState): string {
  switch (state.kind) {
    case "loading":
      return "Checking API readiness";
    case "connection-error":
      return "Connection error";
    case "invalid-response":
      return "Unexpected health response";
    case "ready":
      return "Research API ready";
    case "degraded":
      return "Research API degraded";
    case "unready":
      return "Research API unready";
  }
}

function details(state: WorkspaceState): string {
  if (state.kind === "loading")
    return "Connecting to the local read-only research API.";
  if (state.kind === "connection-error") return state.message;
  if (state.kind === "invalid-response") {
    return "The API responded, but its readiness payload could not be verified.";
  }
  if (state.kind === "ready") {
    return "The read-only research API and background-job capability reported ready.";
  }
  if (state.kind === "degraded") {
    return "The API is partially available. No unavailable capability is represented as ready.";
  }
  return "Research requests are unavailable until required dependencies recover.";
}

function stateClass(state: WorkspaceState): string {
  return state.kind === "connection-error" || state.kind === "invalid-response"
    ? "error"
    : state.kind;
}

function renderReadiness(readiness: ApiReadiness): string {
  const dependency = (
    name: string,
    value: ApiReadiness["dependencies"]["postgres"],
  ) => `
    <li><span>${name}</span><span class="badge ${value.status}">${value.status}</span></li>`;
  return `
    <dl class="status-grid" aria-label="API readiness details">
      <div><dt>Last checked</dt><dd><time datetime="${readiness.checkedAt}">${new Date(readiness.checkedAt).toLocaleString()}</time></dd></div>
      <div><dt>Read-only research</dt><dd><span class="badge ${readiness.capabilities.readOnlyApi}">${readiness.capabilities.readOnlyApi}</span></dd></div>
      <div><dt>Background jobs</dt><dd><span class="badge ${readiness.capabilities.backgroundJobs}">${readiness.capabilities.backgroundJobs}</span></dd></div>
    </dl>
    <h3>Dependencies</h3>
    <ul class="dependency-list">
      ${dependency("Postgres", readiness.dependencies.postgres)}
      ${dependency("Redis", readiness.dependencies.redis)}
    </ul>`;
}

function render(state: WorkspaceState): void {
  const readinessDetails =
    "readiness" in state ? renderReadiness(state.readiness) : "";
  appElement.innerHTML = `
    <main class="workspace">
      <header class="masthead">
        <p class="eyebrow">Tendy Spider · Research workspace</p>
        <h1>Evidence before conclusions.</h1>
        <p class="intro">A read-only workspace for provider-neutral market research. Market data is not loaded until its source, timestamps, freshness, and adjustment mode can be shown.</p>
      </header>
      <section class="status-card ${stateClass(state)}" aria-labelledby="api-status-title">
        <div class="status-heading">
          <div><p class="eyebrow">System state</p><h2 id="api-status-title">${statusLabel(state)}</h2></div>
          <span class="status-dot" aria-hidden="true"></span>
        </div>
        <p id="api-status-message">${details(state)}</p>
        ${readinessDetails}
        <button type="button" id="retry-health">Check again</button>
      </section>
      <section class="guidance" aria-labelledby="workspace-guidance-title">
        <h2 id="workspace-guidance-title">Research safeguards</h2>
        <ul>
          <li><strong>Data state is explicit:</strong> loading, empty, stale, partial, contradictory, and error results will be labeled in the workspace.</li>
          <li><strong>Delayed or end-of-day data stays labeled:</strong> this shell does not present market prices as live.</li>
          <li><strong>Evidence remains inspectable:</strong> facts require a source identifier or URL, observation time, retrieval time, and freshness status.</li>
          <li><strong>No actions are enabled:</strong> watchlist and alert mutations need explicit confirmation and visible audit history before they can be introduced.</li>
        </ul>
      </section>
      <section class="empty-state" aria-labelledby="research-title">
        <p class="eyebrow">Research canvas</p>
        <h2 id="research-title">No market research loaded</h2>
        <p>When read-only research is available, this area will identify its source, freshness, timestamps, and whether results are complete or partial. It will not calculate authoritative financial metrics in the browser.</p>
      </section>
    </main>`;
  document
    .querySelector<HTMLButtonElement>("#retry-health")
    ?.addEventListener("click", () => void load());
}

async function load(): Promise<void> {
  render({ kind: "loading" });
  try {
    const response = await fetch(readinessUrl(apiBaseUrl), {
      headers: { Accept: "application/json" },
    });
    const readiness = parseApiReadiness((await response.json()) as unknown);
    if (!readiness) {
      render({ kind: "invalid-response" });
      return;
    }
    render({ kind: readiness.status, readiness });
  } catch {
    render({
      kind: "connection-error",
      message: `Could not reach the readiness endpoint at ${readinessUrl(apiBaseUrl)}.`,
    });
  }
}

void load();
