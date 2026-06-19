import type { CitationRecord } from "../api/types";

interface CitationListProps {
  citations: CitationRecord[];
}

export function CitationList({ citations }: CitationListProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Citation Panel</h2>
      </div>
      {citations.length === 0 ? <p className="empty-text">No citations returned.</p> : null}
      <div className="citation-list">
        {citations.map((citation, index) => (
          <article key={`${citation.source_id ?? index}-${citation.chunk_id ?? index}`} className="citation-item">
            <strong>{citation.source_id ?? `S${index + 1}`}</strong>
            <span>{citation.section_title ?? "Untitled section"}</span>
            <code>{citation.document_id ?? "unknown document"}</code>
          </article>
        ))}
      </div>
    </section>
  );
}
