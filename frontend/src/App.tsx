import { useCallback, useEffect, useMemo, useState } from "react";

import { DEFAULT_API_BASE_URL, RagApiError, RagClient } from "./api/ragClient";
import type { ChunkRecord, DebugTrace, DocumentRecord, HealthResponse, QueryResponse, UploadMetadata } from "./api/types";
import { AnswerPanel } from "./components/AnswerPanel";
import { ChunkViewer } from "./components/ChunkViewer";
import { CitationList } from "./components/CitationList";
import { DebugTrace as DebugTracePanel } from "./components/DebugTrace";
import { DocumentList } from "./components/DocumentList";
import { DocumentUpload } from "./components/DocumentUpload";
import { HealthPanel } from "./components/HealthPanel";
import { QueryPanel } from "./components/QueryPanel";

const apiBaseUrl = import.meta.env.VITE_RAG_API_BASE_URL || DEFAULT_API_BASE_URL;

export default function App() {
  const client = useMemo(() => new RagClient(apiBaseUrl), []);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthStatus, setHealthStatus] = useState<"checking" | "online" | "offline">("checking");
  const [healthError, setHealthError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [documentsError, setDocumentsError] = useState<string | null>(null);
  const [documentsLoading, setDocumentsLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [chunks, setChunks] = useState<ChunkRecord[]>([]);
  const [chunksLoading, setChunksLoading] = useState(false);
  const [chunksError, setChunksError] = useState<string | null>(null);
  const [embedding, setEmbedding] = useState(false);
  const [embedResult, setEmbedResult] = useState<string | null>(null);
  const [answer, setAnswer] = useState<QueryResponse | null>(null);
  const [answerError, setAnswerError] = useState<string | null>(null);
  const [debugTrace, setDebugTrace] = useState<DebugTrace | null>(null);
  const [debugError, setDebugError] = useState<string | null>(null);
  const [queryBusy, setQueryBusy] = useState(false);

  const selectedDocument = documents.find((document) => document.id === selectedDocumentId) ?? null;

  const refreshHealth = useCallback(async () => {
    setHealthStatus("checking");
    setHealthError(null);
    try {
      const payload = await client.health();
      setHealth(payload);
      setHealthStatus(payload.status === "ok" ? "online" : "offline");
    } catch (error) {
      setHealth(null);
      setHealthStatus("offline");
      setHealthError(formatError(error));
    }
  }, [client]);

  const refreshDocuments = useCallback(async () => {
    setDocumentsLoading(true);
    setDocumentsError(null);
    try {
      const payload = await client.listDocuments();
      setDocuments(payload);
    } catch (error) {
      setDocuments([]);
      setDocumentsError(formatError(error));
    } finally {
      setDocumentsLoading(false);
    }
  }, [client]);

  const loadChunks = useCallback(
    async (documentId: string) => {
      setChunksLoading(true);
      setChunksError(null);
      setEmbedResult(null);
      try {
        setChunks(await client.listChunks(documentId));
      } catch (error) {
        setChunks([]);
        setChunksError(formatError(error));
      } finally {
        setChunksLoading(false);
      }
    },
    [client]
  );

  useEffect(() => {
    void refreshHealth();
    void refreshDocuments();
  }, [refreshHealth, refreshDocuments]);

  async function uploadDocument(file: File, metadata: UploadMetadata) {
    setUploading(true);
    setUploadError(null);
    try {
      const payload = await client.uploadDocument(file, metadata);
      await refreshDocuments();
      if (payload.document?.id) {
        setSelectedDocumentId(payload.document.id);
        await loadChunks(payload.document.id);
      }
    } catch (error) {
      setUploadError(formatError(error));
    } finally {
      setUploading(false);
    }
  }

  function selectDocument(documentId: string) {
    setSelectedDocumentId(documentId);
    void loadChunks(documentId);
  }

  async function embedSelectedDocument() {
    if (!selectedDocumentId) {
      return;
    }
    setEmbedding(true);
    setEmbedResult(null);
    setChunksError(null);
    try {
      const payload = await client.embedDocument(selectedDocumentId);
      setEmbedResult(`Indexed ${payload.embedded_chunks ?? 0} chunks.`);
    } catch (error) {
      setChunksError(formatError(error));
    } finally {
      setEmbedding(false);
    }
  }

  async function askQuestion(question: string, topK: number) {
    setQueryBusy(true);
    setAnswerError(null);
    setDebugError(null);
    try {
      const queryRequest = { question, top_k: topK };
      setAnswer(await client.query(queryRequest));
      try {
        setDebugTrace(await client.debugQuery(queryRequest));
      } catch (error) {
        setDebugTrace(null);
        setDebugError(formatError(error));
      }
    } catch (error) {
      setAnswer(null);
      setDebugTrace(null);
      setAnswerError(formatError(error));
    } finally {
      setQueryBusy(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <h1>Robust Local RAG Engine</h1>
          <p>LocalLite document ingestion, retrieval, citations, and debug trace.</p>
        </div>
      </header>
      <div className="dashboard-grid">
        <div className="left-column">
          <HealthPanel
            apiBaseUrl={apiBaseUrl}
            health={health}
            status={healthStatus}
            error={healthError}
            onRefresh={refreshHealth}
          />
          <DocumentUpload uploading={uploading} error={uploadError} onUpload={uploadDocument} />
          <DocumentList
            documents={documents}
            selectedDocumentId={selectedDocumentId}
            loading={documentsLoading}
            error={documentsError}
            onRefresh={refreshDocuments}
            onSelect={selectDocument}
          />
        </div>
        <div className="main-column">
          <ChunkViewer
            document={selectedDocument}
            chunks={chunks}
            loading={chunksLoading}
            embedding={embedding}
            error={chunksError}
            embedResult={embedResult}
            onEmbed={embedSelectedDocument}
          />
          <QueryPanel busy={queryBusy} onAsk={askQuestion} />
          <AnswerPanel answer={answer} error={answerError} />
          <CitationList citations={Array.isArray(answer?.citations) ? answer.citations : []} />
          <DebugTracePanel trace={debugTrace} error={debugError} />
        </div>
      </div>
    </main>
  );
}

function formatError(error: unknown): string {
  if (error instanceof RagApiError) {
    return error.status ? `${error.message} (HTTP ${error.status})` : error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Unexpected error.";
}
