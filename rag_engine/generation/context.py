from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    source_id: str
    chunk_id: str
    document_id: str
    section_title: str
    text: str
    score: float


class ContextBuilder:
    def build(self, vector_results: list[dict]) -> dict:
        sources = [
            Source(
                source_id=f"S{index}",
                chunk_id=result["chunk_id"],
                document_id=result["document_id"],
                section_title=result["metadata"]["section_title"],
                text=result["text"],
                score=result["score"],
            )
            for index, result in enumerate(vector_results, start=1)
        ]

        context = "\n\n".join(format_source(source) for source in sources)
        return {
            "context": context,
            "sources": [source.__dict__ for source in sources],
        }


def format_source(source: Source) -> str:
    return (
        f"SOURCE {source.source_id}\n"
        f"chunk_id: {source.chunk_id}\n"
        f"document_id: {source.document_id}\n"
        f"section: {source.section_title}\n"
        f"text:\n{source.text}"
    )
