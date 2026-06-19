import type { ChunkRecord, DocumentRecord } from "../api/types";

interface ChunkViewerProps {
  document: DocumentRecord | null;
  chunks: ChunkRecord[];
  loading: boolean;
  embedding: boolean;
  error: string | null;
  embedResult: string | null;
  onEmbed: () => void;
}

export function ChunkViewer({
  document,
  chunks,
  loading,
  embedding,
  error,
  embedResult,
  onEmbed
}: ChunkViewerProps) {
  return (
    <section className="panel chunk-panel">
      <div className="panel-heading">
        <div>
          <h2>Chunk Viewer</h2>
          <p>{document ? document.title ?? document.file_name ?? document.id : "Select a document"}</p>
        </div>
        <button type="button" onClick={onEmbed} disabled={!document || embedding}>
          {embedding ? "Indexing..." : "Embed / Index"}
        </button>
      </div>
      {loading ? <p className="empty-text">Loading chunks...</p> : null}
      {!loading && document && chunks.length === 0 ? <p className="empty-text">No chunks found.</p> : null}
      {!document ? <p className="empty-text">No document selected.</p> : null}
      <div className="chunk-list">
        {chunks.map((chunk) => (
          <article key={chunk.chunk_id} className="chunk-item">
            <header>
              <strong>{chunk.section_title || "Untitled section"}</strong>
              <span>#{chunk.chunk_index ?? "?"}</span>
            </header>
            <p>{chunk.text || "No chunk text available."}</p>
          </article>
        ))}
      </div>
      {embedResult ? <p className="success-text">{embedResult}</p> : null}
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
