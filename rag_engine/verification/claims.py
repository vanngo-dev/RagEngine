import re

from pydantic import BaseModel, Field


CITATION_PATTERN = re.compile(r"\[(S\d+)\]")
CLAIM_WITH_CITATIONS_PATTERN = re.compile(r"(.+?)\s*((?:\[(?:S\d+)\]\s*)+)")


class StructuredClaim(BaseModel):
    claim_id: str
    claim_text: str
    source_ids: list[str] = Field(default_factory=list)


class ClaimsPayload(BaseModel):
    claims: list[StructuredClaim] = Field(default_factory=list)


def claims_from_answer(answer: str) -> ClaimsPayload:
    claims = []
    matches = list(CLAIM_WITH_CITATIONS_PATTERN.finditer(answer))

    if matches:
        for index, match in enumerate(matches, start=1):
            claim_text = match.group(1).strip()
            source_ids = CITATION_PATTERN.findall(match.group(2))
            if claim_text:
                claims.append(
                    StructuredClaim(
                        claim_id=f"c{index}",
                        claim_text=claim_text,
                        source_ids=source_ids,
                    )
                )
        return ClaimsPayload(claims=claims)

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=\.)\s+", answer)
        if sentence.strip()
    ]

    for index, sentence in enumerate(sentences, start=1):
        source_ids = CITATION_PATTERN.findall(sentence)
        claim_text = CITATION_PATTERN.sub("", sentence).strip()
        if claim_text:
            claims.append(
                StructuredClaim(
                    claim_id=f"c{index}",
                    claim_text=claim_text,
                    source_ids=source_ids,
                )
            )

    return ClaimsPayload(claims=claims)


def render_claims(claims: list[StructuredClaim]) -> str:
    rendered = []
    for claim in claims:
        citations = " ".join(f"[{source_id}]" for source_id in claim.source_ids)
        rendered.append(f"{claim.claim_text} {citations}".strip())

    return " ".join(rendered)
