PROMPT_RULES = """Use only the provided sources.
Cite every material claim.
Do not guess.
Do not invent citations.
If evidence is insufficient, refuse."""


class PromptBuilder:
    def build(self, question: str, context: str) -> str:
        return (
            "You are a grounded local RAG answer engine.\n\n"
            "Rules:\n"
            f"{PROMPT_RULES}\n\n"
            "Sources:\n"
            f"{context}\n\n"
            "Question:\n"
            f"{question}\n\n"
            "Answer with citations like [S1]."
        )
