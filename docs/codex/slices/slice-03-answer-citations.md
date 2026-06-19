# Slice 03 — First Answer With Citations

## Goal

Generate grounded answers from retrieved evidence using a local LLM provider.

This slice adds the first answer-generation path while enforcing basic citation behavior.

## Build Only This

- `LLMProvider` interface
- `MockLLMProvider` for tests
- Ollama-compatible provider
- `ContextBuilder`
- `PromptBuilder`
- `POST /query`
- `docs/youtube/phase-03.md`

Do not build hybrid retrieval, verification, or confidence scoring in this slice.

## Requirements

Implement this query flow:

```text
question
→ vector search
→ context builder
→ prompt builder
→ LLM provider
→ answer with citations
```

Prompt rules must include:

```text
Use only the provided sources.
Cite every material claim.
Do not guess.
Do not invent citations.
If evidence is insufficient, refuse.
```

Implementation requirements:

- Use vector search results as source evidence.
- Build context with stable source IDs.
- Ensure prompts include source IDs and citation rules.
- Use a mock LLM provider for deterministic tests.
- Add an Ollama-compatible provider for local use.
- If retrieval returns no useful evidence, return a refusal instead of guessing.
- Return answer and citations from `/query`.
- Keep citation behavior simple and testable.

## API Endpoints Required

Implement:

```http
POST /query
```

Request body:

```json
{
  "question": "What is this document about?"
}
```

Response body must include:

```text
answer
citations
```

## Tests Required

Add tests for:

- empty retrieval refuses
- context builder includes source IDs
- prompt includes citation rules
- mocked LLM returns cited answer
- `/query` response includes answer and citations

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\"}"

pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-03.md
```

The documentation must include:

- phase title: `Phase 03 — First Answer With Citations`
- video goal
- query flow walkthrough
- LLM provider interface explanation
- context builder explanation
- prompt rules explanation
- citation response demo
- test commands
- validation checklist

## Acceptance Criteria

- `/query` accepts a question.
- `/query` retrieves vector evidence.
- Context includes source IDs.
- Prompt includes the citation and refusal rules.
- Mocked tests produce cited answers.
- Empty retrieval refuses.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 03.

Do not implement hybrid retrieval, keyword search, citation verifier, structured claims, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
