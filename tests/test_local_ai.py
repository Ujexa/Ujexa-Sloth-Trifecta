import requests
import pytest

from toolkit.local_ai import generate, health_check


class FakeResponse:
    status_code = 200
    text = ""

    def raise_for_status(self):
        pass

    def json(self):
        return {"response": "hello"}


def test_generate_sends_request(monkeypatch):
    def fake_post(url, json, timeout):
        assert url == "http://localhost:11434/api/generate"
        assert json["model"] == "gemma3:1b"
        assert json["stream"] is False
        assert json["options"]["temperature"] == 0.2
        return FakeResponse()

    monkeypatch.setattr("toolkit.local_ai.requests.post", fake_post)
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "gemma3:1b")
    assert generate("test") == "hello"


def test_empty_prompt_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        generate("  ")


def test_connection_error_has_actionable_message(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("offline")

    monkeypatch.setattr("toolkit.local_ai.requests.post", fake_post)
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")
    with pytest.raises(RuntimeError, match="Cannot reach Ollama"):
        generate("test")


def test_health_check_recognizes_installed_model(monkeypatch):
    class TagsResponse(FakeResponse):
        def json(self):
            return {"models": [{"name": "gemma3:1b"}]}

    monkeypatch.setattr("toolkit.local_ai.requests.get", lambda *args, **kwargs: TagsResponse())
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "gemma3:1b")
    assert health_check()["model_available"] is True
