from pathlib import Path

from rag_engine.ingestion.chunker import DEFAULT_SECTION, TextBlock


SUPPORTED_EXTENSIONS = {".txt", ".md"}


def validate_supported_file(file_name: str) -> str:
    suffix = Path(file_name).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{suffix}'. Supported types: {supported}")

    return suffix.lstrip(".")


def decode_text(content: bytes) -> str:
    try:
        return content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def parse_text_file(content: bytes) -> list[TextBlock]:
    text = decode_text(content)
    return [
        TextBlock(text=paragraph.strip(), section_title=DEFAULT_SECTION)
        for paragraph in split_paragraphs(text)
    ]


def parse_markdown_file(content: bytes) -> list[TextBlock]:
    text = decode_text(content)
    blocks: list[TextBlock] = []
    section_title = DEFAULT_SECTION
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            paragraph = " ".join(line.strip() for line in paragraph_lines).strip()
            if paragraph:
                blocks.append(TextBlock(text=paragraph, section_title=section_title))
            paragraph_lines.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            heading = stripped.lstrip("#").strip()
            if heading:
                section_title = heading
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    return blocks


def parse_document(file_name: str, content: bytes) -> list[TextBlock]:
    source_type = validate_supported_file(file_name)
    if source_type == "md":
        return parse_markdown_file(content)

    return parse_text_file(content)


def split_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue

        current.append(stripped)

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs
