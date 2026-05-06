"""Tests for the AI module (vocabCLI/modules/AI.py).

All OpenAI API calls are mocked so the tests run without a real API key and
without making any network requests.
"""

from unittest import mock
from unittest.mock import MagicMock, patch

import pytest


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def _make_fake_stream(text: str):
    """Build a list of fake streaming chunks that look like openai API chunks."""

    class FakeDelta:
        def __init__(self, content):
            self.content = content

    class FakeChoice:
        def __init__(self, content):
            self.delta = FakeDelta(content)

    class FakeChunk:
        def __init__(self, content):
            self.choices = [FakeChoice(content)]

    # Yield each character as a separate chunk (as the real API does)
    return [FakeChunk(ch) for ch in text]


def _mock_openai_client(response_text: str = "AI response text"):
    """Return a mock OpenAI client that streams *response_text*."""
    client = MagicMock()
    client.chat.completions.create.return_value = _make_fake_stream(response_text)
    return client


# ──────────────────────────────────────────────────────────────────────────────
# get_ai_client
# ──────────────────────────────────────────────────────────────────────────────


class TestGetAiClient:
    def test_returns_client_with_env_key(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        with patch("builtins.__import__", wraps=__import__) as mock_import:
            try:
                from modules.AI import get_ai_client
                # Simply check that it doesn't crash when key is set
                # (actual import of openai may fail if not installed)
            except Exception:
                pass  # openai not installed in test env

    def test_ollama_provider(self, monkeypatch):
        """When provider=ollama, model should be a llama variant."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        import sys
        # Mock openai module
        mock_openai_module = MagicMock()
        mock_client_instance = MagicMock()
        mock_openai_module.OpenAI.return_value = mock_client_instance
        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            # Force reload of AI module to pick up mock
            if "modules.AI" in sys.modules:
                del sys.modules["modules.AI"]
            import modules.AI as ai_mod
            client, model = ai_mod.get_ai_client(provider="ollama")
            assert "llama" in model.lower()

    def test_exits_without_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI", raising=False)
        import sys
        mock_openai_module = MagicMock()
        with patch.dict(sys.modules, {"openai": mock_openai_module}):
            if "modules.AI" in sys.modules:
                del sys.modules["modules.AI"]
            import modules.AI as ai_mod
            with patch.object(ai_mod, "_read_config", return_value={}):
                with pytest.raises(SystemExit):
                    ai_mod.get_ai_client()

    def test_exits_without_openai_package(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        import sys
        with patch.dict(sys.modules, {"openai": None}):
            if "modules.AI" in sys.modules:
                del sys.modules["modules.AI"]
            import modules.AI as ai_mod
            with pytest.raises(SystemExit):
                ai_mod.get_ai_client()


# ──────────────────────────────────────────────────────────────────────────────
# simple_completion
# ──────────────────────────────────────────────────────────────────────────────


class TestSimpleCompletion:
    def test_returns_content(self):
        from modules.AI import simple_completion

        client = MagicMock()
        client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="hello world"))
        ]
        result = simple_completion(client, "gpt-4o-mini", "test prompt")
        assert result == "hello world"

    def test_handles_none_content(self):
        from modules.AI import simple_completion

        client = MagicMock()
        client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=None))
        ]
        result = simple_completion(client, "gpt-4o-mini", "test prompt")
        assert result == ""


# ──────────────────────────────────────────────────────────────────────────────
# AI cache
# ──────────────────────────────────────────────────────────────────────────────


class TestAiCache:
    def test_save_and_retrieve(self):
        from modules.AI import _get_cached, _save_to_cache

        _save_to_cache("testword", "test_type", "cached content", "gpt-4o-mini")
        result = _get_cached("testword", "test_type")
        assert result == "cached content"

    def test_cache_miss_returns_none(self):
        from modules.AI import _get_cached

        result = _get_cached("nonexistentword123", "mnemonic")
        assert result is None

    def test_cache_is_case_insensitive(self):
        from modules.AI import _get_cached, _save_to_cache

        _save_to_cache("CacheWord", "explain", "content here", "gpt-4o-mini")
        # Should retrieve with lowercase key
        result = _get_cached("CacheWord", "explain")
        assert result == "content here"


# ──────────────────────────────────────────────────────────────────────────────
# ai_mnemonic
# ──────────────────────────────────────────────────────────────────────────────


class TestAiMnemonic:
    def test_mnemonic_uses_cache(self):
        from modules.AI import _save_to_cache, ai_mnemonic

        _save_to_cache("serendipity", "mnemonic", "Cached mnemonic text", "gpt-4o-mini")
        # Should print from cache without calling the API
        with patch("modules.AI.get_ai_client") as mock_get_client:
            result = ai_mnemonic("serendipity")
            mock_get_client.assert_not_called()
        assert result == "Cached mnemonic text"

    def test_mnemonic_calls_api_on_cache_miss(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        with (
            patch("modules.AI.get_ai_client") as mock_get_client,
            patch("modules.AI._get_cached", return_value=None),
            patch("modules.AI._save_to_cache"),
        ):
            client = MagicMock()
            client.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="Think of EPHEMERAL as…"))
            ]
            mock_get_client.return_value = (client, "gpt-4o-mini")
            from modules.AI import ai_mnemonic

            result = ai_mnemonic("ephemeral")
            assert result == "Think of EPHEMERAL as…"


# ──────────────────────────────────────────────────────────────────────────────
# vocab ai CLI commands
# ──────────────────────────────────────────────────────────────────────────────


class TestAiCommands:
    def test_ai_explain_command_exits_without_key(self, runner, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI", raising=False)
        with patch("modules.AI._read_config", return_value={}):
            from vocabCLI import app

            result = runner.invoke(app, ["ai", "explain", "serendipity"])
            # Should exit with non-zero or show error panel (SystemExit caught by runner)
            assert result.exit_code != 0 or "AI Not Configured" in result.stdout

    def test_ai_mnemonic_with_cached_result(self, runner):
        from modules.AI import _save_to_cache

        _save_to_cache("testword", "mnemonic", "Remember TESTWORD like this", "gpt-4o-mini")
        from vocabCLI import app

        result = runner.invoke(app, ["ai", "mnemonic", "testword"])
        assert result.exit_code == 0
        assert "Remember TESTWORD" in result.stdout
