"""Small, configurable client for a local Ollama model."""
import os
from typing import Any

import requests

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "gemma3:1b"


def get_config() -> tuple[str, str]:
    """Return normalized Ollama host and configured model name."""
    host = os.getenv("OLLAMA_HOST", DEFAULT_HOST).strip().rstrip("/")
    model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL).strip()
    if not host or not model:
        raise RuntimeError("OLLAMA_HOST and OLLAMA_MODEL must both be configured.")
    return host, model


def health_check(timeout: int = 3) -> dict[str, Any]:
    """Check whether Ollama is reachable and list installed local models."""
    host, model = get_config()
    try:
        response = requests.get(f"{host}/api/tags", timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        models = [item.get("name", "") for item in payload.get("models", [])]
        return {"ok": True, "host": host, "configured_model": model, "models": models, "model_available": model in models or any(name.split(":")[0] == model.split(":")[0] for name in models)}
    except (requests.exceptions.RequestException, ValueError) as exc:
        return {"ok": False, "host": host, "configured_model": model, "models": [], "model_available": False, "error": str(exc)}


def generate(prompt: str, timeout: int = 180, *, temperature: float = 0.2) -> str:
    """Generate text with the model served by the configured Ollama endpoint."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    host, model = get_config()
    try:
        response = requests.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temperature}},
            timeout=timeout,
        )
        if response.status_code == 404:
            raise RuntimeError(f"Ollama could not find the endpoint or model. Confirm '{model}' is installed with `ollama list`.")
        response.raise_for_status()
        data = response.json()
        result = data.get("response", "").strip()
        if not result:
            raise RuntimeError("The model returned an empty response. Try a shorter input or another model.")
        return result
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(f"Cannot reach Ollama at {host}. Start Ollama and check OLLAMA_HOST.") from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("The model took too long to respond. Try shorter input or a smaller model.") from exc
    except requests.exceptions.HTTPError as exc:
        detail = response.text[:300] if response.text else str(exc)
        raise RuntimeError(f"Ollama request failed ({response.status_code}): {detail}") from exc
    except ValueError as exc:
        raise RuntimeError("Ollama returned an unexpected response. Check the Ollama version and endpoint.") from exc
