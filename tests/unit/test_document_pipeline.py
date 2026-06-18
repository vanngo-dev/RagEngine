from rag_engine.ingestion.chunker import build_embedding_text, chunk_blocks
from rag_engine.ingestion.parsers import parse_document


def test_markdown_parser_uses_heading_as_section() -> None:
    blocks = parse_document(
        "sample.md",
        b"# Overview\n\nThis document explains the policy.",
    )

    assert blocks[0].section_title == "Overview"
    assert blocks[0].text == "This document explains the policy."


def test_chunk_embedding_text_keeps_context_out_of_text() -> None:
    blocks = parse_document(
        "sample.md",
        b"# Overview\n\nThis document explains the policy.",
    )
    chunks = chunk_blocks(blocks)

    embedding_text = build_embedding_text(
        title="sample",
        source_type="md",
        section_title=chunks[0].section_title,
        text=chunks[0].text,
    )

    assert "Document: sample" in embedding_text
    assert "Document Type: md" in embedding_text
    assert "Section: Overview" in embedding_text
    assert not chunks[0].text.startswith("Document:")
