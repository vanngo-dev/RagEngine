from rag_engine.verification.confidence import ConfidenceScorer


def base_trace() -> dict:
    return {
        "question": "What number is mentioned?",
        "selected_evidence": {
            "primary_evidence": [{"text": "The number mentioned is 42."}],
            "supporting_evidence": [],
            "weak_evidence": [],
            "conflicting_evidence": [],
        },
        "rerank_results": [{"reranker_score": 0.8}],
        "verification": {"passed": True},
        "injection_warnings": [],
    }


def test_strong_evidence_raises_confidence() -> None:
    result = ConfidenceScorer().score(base_trace())

    assert result["confidence"] >= 0.75
    assert result["confidence_label"] == "high"
    assert result["refusal"] is False


def test_weak_evidence_lowers_confidence() -> None:
    trace = base_trace()
    trace["rerank_results"] = [{"reranker_score": 0.05}]

    result = ConfidenceScorer().score(trace)

    assert result["confidence"] < 0.75
    assert "weak_retrieval" in result["confidence_signals"]["negative"]


def test_failed_citation_lowers_confidence() -> None:
    trace = base_trace()
    trace["verification"] = {"passed": False}

    result = ConfidenceScorer().score(trace)

    assert result["refusal"] is True
    assert "failed_citation" in result["confidence_signals"]["negative"]


def test_conflict_lowers_confidence() -> None:
    trace = base_trace()
    trace["selected_evidence"]["conflicting_evidence"] = [
        {"text": "Conflict: another source disagrees."}
    ]

    result = ConfidenceScorer().score(trace)

    assert "unresolved_conflict" in result["confidence_signals"]["negative"]


def test_prompt_injection_warning_lowers_confidence() -> None:
    trace = base_trace()
    trace["injection_warnings"] = [{"source_id": "S1"}]

    result = ConfidenceScorer().score(trace)

    assert "prompt_injection_warning" in result["confidence_signals"]["negative"]
