from rag_engine.generation.context import ContextBuilder
from rag_engine.generation.llm import MockLLMProvider
from rag_engine.generation.prompts import PromptBuilder
from rag_engine.generation.query import REFUSAL_ANSWER, answer_question


def vector_result() -> dict:
    return {
        "chunk_id": "chunk_1",
        "document_id": "doc_1",
        "text": "The document is about supply chain risk.",
        "score": 0.9,
        "metadata": {
            "section_title": "Overview",
            "status": "uploaded",
            "chunk_index": 0,
            "token_count": 8,
        },
    }


def test_context_builder_includes_source_ids() -> None:
    context = ContextBuilder().build([vector_result()])

    assert "SOURCE S1" in context["context"]
    assert "chunk_id: chunk_1" in context["context"]
    assert context["sources"][0]["source_id"] == "S1"


def test_prompt_includes_citation_rules() -> None:
    prompt = PromptBuilder().build(
        question="What is this about?",
        context="SOURCE S1\ntext:\nEvidence.",
    )

    assert "Use only the provided sources." in prompt
    assert "Cite every material claim." in prompt
    assert "Do not invent citations." in prompt
    assert "If evidence is insufficient, refuse." in prompt


def test_mocked_llm_returns_cited_answer() -> None:
    prompt = PromptBuilder().build(
        question="What is this about?",
        context=ContextBuilder().build([vector_result()])["context"],
    )

    answer = MockLLMProvider().generate(prompt)

    assert answer == "The document is about supply chain risk. [S1]"


class EmptyVectorIndex:
    def search(self, query_vector, top_k):
        return []


class SimpleEmbeddingProvider:
    def embed_text(self, text):
        return [1.0]


def test_empty_retrieval_refuses() -> None:
    response = answer_question(
        question="Unsupported?",
        vector_index=EmptyVectorIndex(),
        embedding_provider=SimpleEmbeddingProvider(),
        llm_provider=MockLLMProvider(),
    )

    assert response["answer"] == REFUSAL_ANSWER
    assert response["citations"] == []
