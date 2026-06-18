import json
import re
from abc import ABC, abstractmethod
from urllib import request


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        match = re.search(r"SOURCE (S\d+).*?text:\n(.+?)(?:\n\nSOURCE|\Z)", prompt, re.S)
        if not match:
            return "I do not have enough evidence to answer that question."

        source_id = match.group(1)
        source_text = extract_untrusted_source_text(match.group(2))
        source_text = " ".join(source_text.split())
        first_sentence = source_text.split(".")[0].strip()
        if not first_sentence:
            return "I do not have enough evidence to answer that question."

        return f"{first_sentence}. [{source_id}]"


class OllamaLLMProvider(LLMProvider):
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        http_request = request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(http_request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))

        return body.get("response", "").strip()


def get_llm_provider(
    name: str,
    ollama_base_url: str,
    ollama_model: str,
) -> LLMProvider:
    normalized = name.lower().strip()
    if normalized == "mock":
        return MockLLMProvider()
    if normalized == "ollama":
        return OllamaLLMProvider(ollama_base_url, ollama_model)

    raise ValueError(f"Unknown LLM provider: {name}")


def extract_untrusted_source_text(source_block: str) -> str:
    start = "BEGIN UNTRUSTED SOURCE CONTENT"
    end = "END UNTRUSTED SOURCE CONTENT"

    if start in source_block and end in source_block:
        return source_block.split(start, 1)[1].split(end, 1)[0].strip()

    return source_block.strip()
