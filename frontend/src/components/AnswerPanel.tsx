import type { QueryResponse } from "../api/types";

interface AnswerPanelProps {
  answer: QueryResponse | null;
  error: string | null;
}

export function AnswerPanel({ answer, error }: AnswerPanelProps) {
  const confidence =
    typeof answer?.confidence === "number" ? `${Math.round(answer.confidence * 100)}%` : "unknown";

  return (
    <section className="panel answer-panel">
      <div className="panel-heading">
        <h2>Answer Panel</h2>
      </div>
      {!answer ? <p className="empty-text">Ask a question to generate an answer.</p> : null}
      {answer ? (
        <>
          <p className="answer-text">{answer.answer || "No answer returned."}</p>
          <dl className="detail-grid">
            <div>
              <dt>Confidence</dt>
              <dd>{confidence}</dd>
            </div>
            <div>
              <dt>Label</dt>
              <dd>{answer.confidence_label ?? "unknown"}</dd>
            </div>
            <div>
              <dt>Refusal</dt>
              <dd>{answer.refusal ? "yes" : "no"}</dd>
            </div>
          </dl>
          {Array.isArray(answer.missing_information) && answer.missing_information.length > 0 ? (
            <div className="callout">
              <strong>Missing information</strong>
              <ul>
                {answer.missing_information.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </>
      ) : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
