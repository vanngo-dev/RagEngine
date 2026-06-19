import type {
  ChunkRecord,
  DebugTrace,
  DocumentRecord,
  HealthResponse,
  QueryRequest,
  QueryResponse,
  UploadMetadata
} from "./types";

export const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

export class RagApiError extends Error {
  readonly status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "RagApiError";
    this.status = status;
  }
}

export class RagClient {
  readonly baseUrl: string;

  constructor(baseUrl: string = DEFAULT_API_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/+$/, "");
  }

  health(): Promise<HealthResponse> {
    return this.request<HealthResponse>("/health");
  }

  async uploadDocument(file: File, metadata: UploadMetadata): Promise<{ document?: DocumentRecord }> {
    const body = new FormData();
    body.append("file", file);
    appendOptional(body, "entity", metadata.entity);
    appendOptional(body, "document_type", metadata.document_type);
    appendOptional(body, "document_date", metadata.document_date);
    appendOptional(body, "document_family_id", metadata.document_family_id);

    return this.request<{ document?: DocumentRecord }>("/documents/upload", {
      method: "POST",
      body
    });
  }

  async listDocuments(): Promise<DocumentRecord[]> {
    const payload = await this.request<{ documents?: unknown }>("/documents");
    return Array.isArray(payload.documents) ? (payload.documents as DocumentRecord[]) : [];
  }

  async listChunks(documentId: string): Promise<ChunkRecord[]> {
    const payload = await this.request<{ chunks?: unknown }>(`/documents/${encodeURIComponent(documentId)}/chunks`);
    return Array.isArray(payload.chunks) ? (payload.chunks as ChunkRecord[]) : [];
  }

  embedDocument(documentId: string): Promise<{ document_id?: string; embedded_chunks?: number }> {
    return this.request<{ document_id?: string; embedded_chunks?: number }>(
      `/documents/${encodeURIComponent(documentId)}/embed`,
      { method: "POST" }
    );
  }

  query(request: QueryRequest): Promise<QueryResponse> {
    return this.request<QueryResponse>("/query", {
      method: "POST",
      headers: jsonHeaders(),
      body: JSON.stringify(request)
    });
  }

  debugQuery(request: QueryRequest): Promise<DebugTrace> {
    return this.request<DebugTrace>("/query/debug", {
      method: "POST",
      headers: jsonHeaders(),
      body: JSON.stringify(request)
    });
  }

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    let response: Response;
    try {
      response = await fetch(`${this.baseUrl}${path}`, init);
    } catch (error) {
      throw new RagApiError(
        error instanceof Error
          ? `Could not reach backend: ${error.message}`
          : "Could not reach backend"
      );
    }

    const payload = await parseJsonSafely(response);
    if (!response.ok) {
      const message = extractErrorMessage(payload) ?? `Request failed with HTTP ${response.status}`;
      throw new RagApiError(message, response.status);
    }

    if (!isRecord(payload)) {
      throw new RagApiError("Backend returned an unexpected response shape.", response.status);
    }

    return payload as T;
  }
}

function appendOptional(body: FormData, key: string, value: string | undefined): void {
  if (value && value.trim()) {
    body.append(key, value.trim());
  }
}

function jsonHeaders(): HeadersInit {
  return {
    "Content-Type": "application/json"
  };
}

async function parseJsonSafely(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text) as unknown;
  } catch {
    throw new RagApiError("Backend returned invalid JSON.", response.status);
  }
}

function extractErrorMessage(payload: unknown): string | undefined {
  if (!isRecord(payload)) {
    return undefined;
  }
  const detail = payload.detail;
  if (typeof detail === "string") {
    return detail;
  }
  return undefined;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
