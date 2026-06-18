# Phase 03 — First Answer With Citations

## Video Goal

Generate the first grounded answer from retrieved vector evidence and return citations.

## Query Flow Walkthrough

The `/query` endpoint embeds the question, searches the vector index, builds a source context with stable source IDs, builds a citation-focused prompt, calls the configured LLM provider, and extracts cited sources from the answer.

## LLM Provider Interface

The generation layer now has an `LLMProvider` interface. Tests use `MockLLMProvider` for deterministic cited answers. Local runs can select the Ollama-compatible provider with configuration.

## Context Builder

`ContextBuilder` converts vector search results into source blocks labeled `S1`, `S2`, and so on. These stable source IDs make citation extraction simple and predictable.

## Prompt Rules

The prompt tells the model to:

- use only provided sources
- cite every material claim
- avoid guessing
- avoid invented citations
- refuse when evidence is insufficient

## Citation Response Demo

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\"}"
```

The response includes:

```text
answer
citations
```

## Test Commands

```bash
pytest
```

## Validation Checklist

- `/query` accepts a question
- vector evidence is retrieved
- context includes source IDs
- prompt includes citation and refusal rules
- mocked LLM returns a cited answer
- empty retrieval refuses
