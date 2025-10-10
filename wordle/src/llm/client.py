import os
import time
from dataclasses import dataclass
from typing import Any, Dict

import requests
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    temperature: float
    max_tokens: int


def _read_env() -> LLMConfig:
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    model = os.getenv("LLM_MODEL", "llama3.2:3b").strip()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", "64"))
    return LLMConfig(
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


class LocalLLMClient:
    """Wrapper around the local Ollama HTTP API."""

    def __init__(self) -> None:
        self.config = _read_env()
        if self.config.provider != "ollama":
            raise ValueError(
                f"Unsupported LLM provider '{self.config.provider}'. Only local Ollama is allowed."
            )
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def chat(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Send a single chat completion request and return the parsed response."""
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
            },
            "stream": False,
        }

        url = f"{self.base_url.rstrip('/')}/api/chat"
        start = time.perf_counter()
        try:
            response = requests.post(url, json=payload, timeout=60)
        except requests.ConnectionError as exc:
            raise ConnectionError(
                f"Failed to connect to Ollama at '{self.base_url}'. "
                "Ensure the Ollama server is running locally."
            ) from exc
        except requests.Timeout as exc:
            raise TimeoutError(
                "Timed out while waiting for a response from the local Ollama server."
            ) from exc

        latency = time.perf_counter() - start
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                f"Ollama returned HTTP {response.status_code}: {response.text}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Failed to decode JSON from Ollama response."
            ) from exc

        error_msg = data.get("error")
        if error_msg:
            if error_msg == "model_not_found":
                raise RuntimeError(
                    f"The model '{self.config.model}' is not available in the local Ollama instance."
                )
            raise RuntimeError(f"Ollama returned an error: {error_msg}")

        message = data.get("message") or {}
        content = message.get("content", "").strip()
        if not content:
            raise RuntimeError(
                "Ollama response did not contain any text. "
                f"Request payload: model={self.config.model}"
            )

        return {
            "text": content,
            "latency_s": latency,
            "raw": data,
        }
