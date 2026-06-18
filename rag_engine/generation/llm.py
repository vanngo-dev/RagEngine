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
        source_text = " ".join(match.group(2).split())
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
