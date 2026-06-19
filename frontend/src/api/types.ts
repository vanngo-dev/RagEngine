export type UnknownRecord = Record<string, unknown>;

export interface HealthResponse extends UnknownRecord {
  status?: string;
  service?: string;
  version?: string;
}

export interface DocumentRecord extends UnknownRecord {
  id: string;
  title?: string;
  file_name?: string;
  source_type?: string;
  status?: string;
  entity?: string;
  document_type?: string;
  document_date?: string;
  document_family_id?: string;
  created_at?: string;
}

export interface ChunkRecord extends UnknownRecord {
  chunk_id: string;
  document_id: string;
  text?: string;
  embedding_text?: string;
  section_title?: string;
  chunk_index?: number;
  token_count?: number;
}

export interface SearchResult extends UnknownRecord {
  chunk_id?: string;
  document_id?: string;
  text?: string;
  section_title?: string;
  score?: number;
}

export interface CitationRecord extends UnknownRecord {
  source_id?: string;
  chunk_id?: string;
  document_id?: string;
  section_title?: string;
}

export interface QueryResponse extends UnknownRecord {
  answer?: string;
  citations?: CitationRecord[];
  confidence?: number;
  confidence_label?: string;
  refusal?: boolean;
  missing_information?: string[];
}

export interface DebugTrace extends QueryResponse {
  question?: string;
  vector_results?: SearchResult[];
  hybrid_results?: SearchResult[];
  rerank_results?: SearchResult[];
  selected_evidence?: UnknownRecord;
  injection_warnings?: string[];
  selected_context?: string;
  prompt_preview?: string;
  structured_claims?: UnknownRecord;
  verification?: UnknownRecord;
  verification_attempts?: number;
}

export interface UploadMetadata {
  entity?: string;
  document_type?: string;
  document_date?: string;
  document_family_id?: string;
}

export interface QueryRequest {
  question: string;
  top_k: number;
}

export interface ApiErrorPayload {
  message: string;
  status?: number;
}
