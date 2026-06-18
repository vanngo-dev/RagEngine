from rag_engine.generation.verified_answer import generate_verified_answer
from rag_engine.verification.citation_verifier import CitationVerifier
from rag_engine.verification.claims import ClaimsPayload, StructuredClaim


def source() -> dict:
    return {
        "source_id": "S1",
        "chunk_id": "chunk_1",
        "document_id": "doc_1",
        "section_title": "Facts",
        "text": "Revenue was 42 on 2025-01-01.",
    }


def verify_claim(claim: StructuredClaim) -> dict:
    payload = ClaimsPayload(claims=[claim])
    return CitationVerifier().verify(payload, [source()])


def test_claim_has_source_ids() -> None:
    claim = StructuredClaim(
        claim_id="c1",
        claim_text="Revenue was 42 on 2025-01-01.",
        source_ids=["S1"],
    )

    assert claim.source_ids == ["S1"]


def test_fake_citation_rejected() -> None:
    result = verify_claim(
        StructuredClaim(claim_id="c1", claim_text="Revenue was 42.", source_ids=["S99"])
    )

    assert result["passed"] is False
    assert "fake_citation" in result["claim_results"][0]["errors"]


def test_missing_citation_rejected() -> None:
    result = verify_claim(
        StructuredClaim(claim_id="c1", claim_text="Revenue was 42.", source_ids=[])
    )

    assert result["passed"] is False
    assert "missing_citation" in result["claim_results"][0]["errors"]


def test_wrong_number_rejected() -> None:
    result = verify_claim(
        StructuredClaim(claim_id="c1", claim_text="Revenue was 43.", source_ids=["S1"])
    )

    assert result["passed"] is False
    assert "wrong_number" in result["claim_results"][0]["errors"]


def test_wrong_date_rejected() -> None:
    result = verify_claim(
        StructuredClaim(
            claim_id="c1",
            claim_text="Revenue was 42 on 2024-01-01.",
            source_ids=["S1"],
        )
    )

    assert result["passed"] is False
    assert "wrong_date" in result["claim_results"][0]["errors"]


def test_unsupported_claim_fails() -> None:
    result = verify_claim(
        StructuredClaim(claim_id="c1", claim_text="Profit doubled.", source_ids=["S1"])
    )

    assert result["passed"] is False
    assert "unsupported_claim" in result["claim_results"][0]["errors"]


class AlwaysBadLLM:
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, prompt: str) -> str:
        self.calls += 1
        return "Profit doubled. [S1]"


def test_retry_cap_and_second_failure_refuses() -> None:
    llm = AlwaysBadLLM()

    response = generate_verified_answer(
        prompt="prompt",
        sources=[source()],
        llm_provider=llm,
    )

    assert llm.calls == 2
    assert response["verification_attempts"] == 2
    assert response["refused_after_verification"] is True
    assert response["answer"] == "I do not have enough evidence to answer that question."
