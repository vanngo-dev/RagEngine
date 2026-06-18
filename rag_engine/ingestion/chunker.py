from dataclasses import dataclass


DEFAULT_SECTION = "Document"


@dataclass(frozen=True)
class TextBlock:
    text: str
    section_title: str = DEFAULT_SECTION


@dataclass(frozen=True)
class Chunk:
    text: str
    section_title: str
    chunk_index: int
    token_count: int


def count_tokens(text: str) -> int:
    return len(text.split())


def build_embedding_text(
    title: str,
    source_type: str,
    section_title: str,
    text: str,
) -> str:
    return (
        f"Document: {title}\n"
        f"Document Type: {source_type}\n"
        f"Section: {section_title}\n\n"
        f"{text}"
    )


def chunk_blocks(blocks: list[TextBlock], max_tokens: int = 180) -> list[Chunk]:
    chunks: list[Chunk] = []

    for block in blocks:
        section_title = block.section_title or DEFAULT_SECTION
        words = block.text.split()
        if not words:
            continue

        for start in range(0, len(words), max_tokens):
            text = " ".join(words[start : start + max_tokens]).strip()
            if not text:
                continue

            chunks.append(
                Chunk(
                    text=text,
                    section_title=section_title,
                    chunk_index=len(chunks),
                    token_count=count_tokens(text),
                )
            )

    return chunks
