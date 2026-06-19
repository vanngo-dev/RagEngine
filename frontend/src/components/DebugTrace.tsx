import type { DebugTrace as DebugTracePayload } from "../api/types";

interface DebugTraceProps {
  trace: DebugTracePayload | null;
  error: string | null;
}

export function DebugTrace({ trace, error }: DebugTraceProps) {
  return (
    <section className="panel debug-panel">
      <div className="panel-heading">
        <h2>Debug Trace Panel</h2>
      </div>
      {!trace ? <p className="empty-text">Debug details appear after a question runs.</p> : null}
      {trace ? (
        <>
          <dl className="detail-grid">
            <div>
              <dt>Vector</dt>
              <dd>{trace.vector_results?.length ?? 0}</dd>
            </div>
            <div>
              <dt>Hybrid</dt>
              <dd>{trace.hybrid_results?.length ?? 0}</dd>
            </div>
            <div>
              <dt>Rerank</dt>
              <dd>{trace.rerank_results?.length ?? 0}</dd>
            </div>
            <div>
              <dt>Attempts</dt>
              <dd>{trace.verification_attempts ?? 0}</dd>
            </div>
          </dl>
          {Array.isArray(trace.injection_warnings) && trace.injection_warnings.length > 0 ? (
            <div className="callout warning">
              <strong>Injection warnings</strong>
              <ul>
                {trace.injection_warnings.map((warning) => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            </div>
          ) : null}
          <details>
            <summary>Selected context</summary>
            <pre>{trace.selected_context || "No context returned."}</pre>
          </details>
          <details>
            <summary>Prompt preview</summary>
            <pre>{trace.prompt_preview || "No prompt preview returned."}</pre>
          </details>
          <details>
            <summary>Raw trace</summary>
            <pre>{JSON.stringify(trace, null, 2)}</pre>
          </details>
        </>
      ) : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
