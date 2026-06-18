from rag_engine.generation.llm import LLMProvider
from rag_engine.verification.citation_verifier import CitationVerifier
from rag_engine.verification.claims import claims_from_answer, render_claims


REFUSAL_ANSWER = "I do not have enough evidence to answer that question."


def generate_verified_answer(
    prompt: str,
    sources: list[dict],
    llm_provider: LLMProvider,
    max_attempts: int = 2,
) -> dict:
    verifier = CitationVerifier()
    last_claims = None
    last_verification = None

    for attempt in range(1, max_attempts + 1):
        draft_answer = llm_provider.generate(prompt)
        claims_payload = claims_from_answer(draft_answer)
        verification = verifier.verify(claims_payload, sources)
        last_claims = claims_payload
        last_verification = verification

        if verification["passed"]:
            return {
                "answer": render_claims(claims_payload.claims),
                "structured_claims": claims_payload.model_dump(),
                "verification": verification,
                "verification_attempts": attempt,
                "refused_after_verification": False,
            }

    return {
        "answer": REFUSAL_ANSWER,
        "structured_claims": last_claims.model_dump() if last_claims else {"claims": []},
        "verification": last_verification or {"passed": False, "claim_results": []},
        "verification_attempts": max_attempts,
        "refused_after_verification": True,
    }
