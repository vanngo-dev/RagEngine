CONFLICT_PATTERNS = (
    "conflict:",
    "conflicts with",
    "contradicts",
    "disagrees with",
)


class EvidenceSelector:
    def __init__(self, max_per_section: int = 2) -> None:
        self.max_per_section = max_per_section

    def select(self, reranked_candidates: list[dict]) -> dict:
        selected = apply_section_diversity(reranked_candidates, self.max_per_section)
        evidence = {
            "primary_evidence": [],
            "supporting_evidence": [],
            "weak_evidence": [],
            "conflicting_evidence": [],
        }

        for index, candidate in enumerate(selected):
            item = dict(candidate)
            item["conflict_flag"] = conflict_flag(item["text"])

            if item["conflict_flag"] != "none":
                evidence["conflicting_evidence"].append(item)
            elif index == 0:
                evidence["primary_evidence"].append(item)
            elif item.get("reranker_score", 0.0) >= 0.35:
                evidence["supporting_evidence"].append(item)
            else:
                evidence["weak_evidence"].append(item)

        return evidence


def apply_section_diversity(candidates: list[dict], max_per_section: int) -> list[dict]:
    counts: dict[tuple[str, str], int] = {}
    selected = []

    for candidate in candidates:
        metadata = candidate.get("metadata", {})
        key = (
            candidate.get("document_id", ""),
            metadata.get("section_title", ""),
        )
        count = counts.get(key, 0)
        if count >= max_per_section:
            continue

        counts[key] = count + 1
        selected.append(candidate)

    return selected


def conflict_flag(text: str) -> str:
    lowered = text.lower()
    for pattern in CONFLICT_PATTERNS:
        if pattern in lowered:
            return "possible_conflict"
    return "none"


def flatten_selected_evidence(selected_evidence: dict) -> list[dict]:
    return (
        selected_evidence["primary_evidence"]
        + selected_evidence["supporting_evidence"]
        + selected_evidence["conflicting_evidence"]
        + selected_evidence["weak_evidence"]
    )
