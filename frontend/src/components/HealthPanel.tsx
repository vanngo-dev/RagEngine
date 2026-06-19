import type { HealthResponse } from "../api/types";

interface HealthPanelProps {
  apiBaseUrl: string;
  health: HealthResponse | null;
  status: "checking" | "online" | "offline";
  error: string | null;
  onRefresh: () => void;
}

export function HealthPanel({ apiBaseUrl, health, status, error, onRefresh }: HealthPanelProps) {
  return (
    <section className="panel health-panel">
      <div className="panel-heading">
        <div>
          <h2>Backend Status</h2>
          <p>{apiBaseUrl}</p>
        </div>
        <button type="button" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      <div className={`status-badge status-${status}`}>{status}</div>
      {health ? (
        <dl className="detail-grid">
          <div>
            <dt>Service</dt>
            <dd>{health.service ?? "unknown"}</dd>
          </div>
          <div>
            <dt>Version</dt>
            <dd>{health.version ?? "unknown"}</dd>
          </div>
        </dl>
      ) : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
