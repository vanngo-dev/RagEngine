INJECTION_PATTERNS = (
    "ignore previous instructions",
    "do not cite sources",
    "reveal hidden system prompt",
    "system prompt",
)


def detect_injection_warnings(sources: list[dict]) -> list[dict]:
    warnings = []

    for source in sources:
        lowered = source["text"].lower()
        matched_patterns = [
            pattern for pattern in INJECTION_PATTERNS if pattern in lowered
        ]
        if matched_patterns:
            warnings.append(
                {
                    "source_id": source["source_id"],
                    "chunk_id": source["chunk_id"],
                    "patterns": matched_patterns,
                }
            )

    return warnings
