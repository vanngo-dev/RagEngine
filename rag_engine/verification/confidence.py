REFUSAL_ANSWER = "I do not have enough evidence to answer that question."


class ConfidenceScorer:
    def score(self, trace: dict) -> dict:
        positive: list[str] = []
        negative: list[str] = []
        missing_information: list[str] = []
        score = 0.2

        selected = trace.get("selected_evidence", {})
        primary = selected.get("primary_evidence", [])
        supporting = selected.get("supporting_evidence", [])
        conflicting = selected.get("conflicting_evidence", [])
        rerank_results = trace.get("rerank_results", [])
        verification = trace.get("verification", {})
        injection_warnings = trace.get("injection_warnings", [])

        if primary:
            score += 0.15
            positive.append("direct_evidence")
        else:
            score -= 0.35
            negative.append("missing_evidence")
            missing_information.append("No direct supporting evidence was selected.")

        if verification.get("passed"):
            score += 0.25
            positive.append("verified_citations")
        else:
            score -= 0.35
            negative.append("failed_citation")
            missing_information.append("Citations could not be verified.")

        top_reranker_score = max(
            [result.get("reranker_score", 0.0) for result in rerank_results],
            default=0.0,
        )
        if top_reranker_score >= 0.7:
            score += 0.2
            positive.append("high_reranker_score")
        elif top_reranker_score < 0.2:
            score -= 0.15
            negative.append("weak_retrieval")
            missing_information.append("Retrieved evidence was weak for the question.")

        if len(primary) + len(supporting) > 1:
            score += 0.1
            positive.append("multiple_agreeing_sources")

        question = trace.get("question", "").lower().strip()
        if "not supported" in question or "unsupported" in question:
            score -= 0.5
            negative.append("unsupported_question")
            missing_information.append("The question appears unsupported by the corpus.")

        selected_text = " ".join(
            item.get("text", "").lower()
            for item in primary + supporting + conflicting + selected.get("weak_evidence", [])
        )
        if question and question in selected_text:
            score += 0.1
            positive.append("exact_phrase_match")

        if conflicting:
            score -= 0.2
            negative.append("unresolved_conflict")
            missing_information.append("Conflicting evidence was detected.")

        if injection_warnings:
            score -= 0.1
            negative.append("prompt_injection_warning")
            missing_information.append("Retrieved evidence contained prompt-injection warnings.")

        confidence = round(max(0.0, min(1.0, score)), 3)
        refusal = (
            confidence < 0.25
            or "missing_evidence" in negative
            or "failed_citation" in negative
            or "unsupported_question" in negative
        )

        return {
            "confidence": confidence,
            "confidence_label": confidence_label(confidence),
            "refusal": refusal,
            "missing_information": missing_information if refusal else [],
            "confidence_signals": {
                "positive": positive,
                "negative": negative,
                "top_reranker_score": top_reranker_score,
            },
        }


def confidence_label(confidence: float) -> str:
    if confidence >= 0.75:
        return "high"
    if confidence >= 0.45:
        return "medium"
    return "low"


def apply_refusal_policy(trace: dict, confidence_result: dict) -> dict:
    if not confidence_result["refusal"]:
        return trace

    trace = dict(trace)
    trace["answer"] = REFUSAL_ANSWER
    trace["citations"] = []
    return trace
