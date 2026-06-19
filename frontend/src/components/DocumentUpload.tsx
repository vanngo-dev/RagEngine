import { FormEvent, useState } from "react";

import type { UploadMetadata } from "../api/types";

interface DocumentUploadProps {
  uploading: boolean;
  error: string | null;
  onUpload: (file: File, metadata: UploadMetadata) => Promise<void>;
}

export function DocumentUpload({ uploading, error, onUpload }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<UploadMetadata>({});

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      return;
    }
    await onUpload(file, metadata);
    setFile(null);
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Document Upload</h2>
      </div>
      <form className="stack" onSubmit={submit}>
        <label>
          File
          <input
            type="file"
            accept=".txt,.md,text/plain,text/markdown"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
        </label>
        <div className="form-grid">
          <label>
            Entity
            <input
              value={metadata.entity ?? ""}
              onChange={(event) => setMetadata({ ...metadata, entity: event.target.value })}
            />
          </label>
          <label>
            Type
            <input
              value={metadata.document_type ?? ""}
              onChange={(event) => setMetadata({ ...metadata, document_type: event.target.value })}
            />
          </label>
          <label>
            Date
            <input
              value={metadata.document_date ?? ""}
              placeholder="YYYY-MM-DD"
              onChange={(event) => setMetadata({ ...metadata, document_date: event.target.value })}
            />
          </label>
          <label>
            Family ID
            <input
              value={metadata.document_family_id ?? ""}
              onChange={(event) => setMetadata({ ...metadata, document_family_id: event.target.value })}
            />
          </label>
        </div>
        <button type="submit" disabled={!file || uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>
      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
