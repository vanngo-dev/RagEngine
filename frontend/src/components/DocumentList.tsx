import type { DocumentRecord } from "../api/types";

interface DocumentListProps {
  documents: DocumentRecord[];
  selectedDocumentId: string | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
  onSelect: (documentId: string) => void;
}

export function DocumentList({
  documents,
  selectedDocumentId,
  loading,
  error,
  onRefresh,
  onSelect
}: DocumentListProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Document List</h2>
        <button type="button" onClick={onRefresh} disabled={loading}>
          Refresh
        </button>
      </div>
      {documents.length === 0 ? <p className="empty-text">No documents found.</p> : null}
      <div className="document-list">
        {documents.map((document) => (
          <button
            type="button"
            key={document.id}
            className={document.id === selectedDocumentId ? "document-row selected" : "document-row"}
            onClick={() => onSelect(document.id)}
          >
            <span className="document-title">{document.title ?? document.file_name ?? document.id}</span>
            <span>{document.status ?? "unknown"}</span>
            <span>{document.entity || document.document_type || document.source_type || "unlabeled"}</span>
          </button>
        ))}
      </div>
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
