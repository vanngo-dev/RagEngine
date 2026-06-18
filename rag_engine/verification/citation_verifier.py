import re
from abc import ABC, abstractmethod

from rag_engine.verification.claims import ClaimsPayload, StructuredClaim


NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?%?\b")
DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "is",
    "the",
    "this",
    "that",
    "to",
    "of",
    "was",
    "were",
}


class SupportVerifier(ABC):
    @abstractmethod
    def supports(self, claim: StructuredClaim, source_text: str) -> bool:
        raise NotImplementedError


class SimpleSupportVerifier(SupportVerifier):
    def supports(self, claim: StructuredClaim, source_text: str) -> bool:
        claim_normalized = normalize_text(claim.claim_text)
        source_normalized = normalize_text(source_text)
        if claim_normalized and claim_normalized in source_normalized:
            return True

        claim_tokens = significant_tokens(claim.claim_text)
        source_tokens = set(TOKEN_PATTERN.findall(source_text.lower()))
        return bool(claim_tokens) and claim_tokens.issubset(source_tokens)


class CitationVerifier:
    def __init__(self, support_verifier: SupportVerifier | None = None) -> None:
        self.support_verifier = support_verifier or SimpleSupportVerifier()

    def verify(self, claims_payload: ClaimsPayload, sources: list[dict]) -> dict:
        source_map = {source["source_id"]: source for source in sources}
        results = []

        for claim in claims_payload.claims:
            results.append(self.verify_claim(claim, source_map))

        passed = bool(results) and all(result["passed"] for result in results)
        return {
            "passed": passed,
            "claim_results": results,
        }

    def verify_claim(self, claim: StructuredClaim, source_map: dict[str, dict]) -> dict:
        errors = []
        cited_sources = []

        if not claim.source_ids:
            errors.append("missing_citation")

        for source_id in claim.source_ids:
            source = source_map.get(source_id)
            if source is None:
                errors.append("fake_citation")
                continue
            cited_sources.append(source)

        combined_source_text = " ".join(source["text"] for source in cited_sources)

        if cited_sources and not any(
            self.support_verifier.supports(claim, source["text"])
            for source in cited_sources
        ):
            errors.append("unsupported_claim")

        for number in NUMBER_PATTERN.findall(claim.claim_text):
            if number not in combined_source_text:
                errors.append("wrong_number")

        for date in DATE_PATTERN.findall(claim.claim_text):
            if date not in combined_source_text:
                errors.append("wrong_date")

        return {
            "claim_id": claim.claim_id,
            "source_ids": claim.source_ids,
            "passed": not errors,
            "errors": sorted(set(errors)),
        }


def normalize_text(text: str) -> str:
    return " ".join(TOKEN_PATTERN.findall(text.lower()))


def significant_tokens(text: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if token not in STOPWORDS
    }
