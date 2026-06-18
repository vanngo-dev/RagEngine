import re

from rag_engine.generation.context import ContextBuilder
from rag_engine.generation.llm import LLMProvider
from rag_engine.generation.prompts import PromptBuilder
from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


REFUSAL_ANSWER = "I do not have enough evidence to answer that question."
CITATION_PATTERN = re.compile(r"\[(S\d+)\]")


def answer_question(
    question: str,
    vector_index: SQLiteVectorIndex,
    embedding_provider: EmbeddingProvider,
    llm_provider: LLMProvider,
    top_k: int = 5,
) -> dict:
    query_vector = embedding_provider.embed_text(question)
    vector_results = vector_index.search(query_vector, top_k=top_k)

    if not vector_results or vector_results[0]["score"] <= 0:
        return {
            "answer": REFUSAL_ANSWER,
            "citations": [],
        }

    context_payload = ContextBuilder().build(vector_results)
    prompt = PromptBuilder().build(question, context_payload["context"])
    answer = llm_provider.generate(prompt)
    citations = extract_citations(answer, context_payload["sources"])

    return {
        "answer": answer,
        "citations": citations,
    }


def extract_citations(answer: str, sources: list[dict]) -> list[dict]:
    source_map = {source["source_id"]: source for source in sources}
    citations = []

    for source_id in dict.fromkeys(CITATION_PATTERN.findall(answer)):
        source = source_map.get(source_id)
        if source is None:
            continue
        citations.append(
            {
                "source_id": source_id,
                "chunk_id": source["chunk_id"],
                "document_id": source["document_id"],
                "section_title": source["section_title"],
            }
        )

    return citations
