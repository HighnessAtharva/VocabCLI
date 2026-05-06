"""Tests for the Config module (vocabCLI/modules/Config.py)."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    """Redirect the config path to a temp directory for each test."""
    monkeypatch.setattr("modules.Config.CONFIG_DIR", tmp_path)
    monkeypatch.setattr("modules.Config.CONFIG_PATH", tmp_path / "config.toml")
    yield tmp_path / "config.toml"


# ──────────────────────────────────────────────────────────────────────────────
# _ensure_config_dir
# ──────────────────────────────────────────────────────────────────────────────


class TestEnsureConfigDir:
    def test_creates_directory(self, tmp_path, monkeypatch):
        new_dir = tmp_path / "new_subdir"
        monkeypatch.setattr("modules.Config.CONFIG_DIR", new_dir)
        monkeypatch.setattr("modules.Config.CONFIG_PATH", new_dir / "config.toml")
        from modules.Config import _ensure_config_dir

        _ensure_config_dir()
        assert new_dir.exists()

    def test_idempotent_on_existing_dir(self, temp_config):
        from modules.Config import _ensure_config_dir

        _ensure_config_dir()
        _ensure_config_dir()  # should not raise


# ──────────────────────────────────────────────────────────────────────────────
# _load_raw
# ──────────────────────────────────────────────────────────────────────────────


class TestLoadRaw:
    def test_creates_default_config(self, temp_config):
        assert not temp_config.exists()
        from modules.Config import _load_raw

        raw = _load_raw()
        assert temp_config.exists()
        assert "[ai]" in raw

    def test_returns_existing_config(self, temp_config):
        temp_config.write_text("[ai]\nprovider = \"openai\"\n")
        from modules.Config import _load_raw

        raw = _load_raw()
        assert 'provider = "openai"' in raw


# ──────────────────────────────────────────────────────────────────────────────
# get_config / set_config
# ──────────────────────────────────────────────────────────────────────────────


class TestGetSetConfig:
    def test_set_and_get_value(self, temp_config):
        from modules.Config import get_config, set_config

        set_config("ai", "provider", "ollama")
        assert get_config("ai", "provider") == "ollama"

    def test_get_missing_key_returns_default(self, temp_config):
        from modules.Config import get_config

        result = get_config("ai", "nonexistent_key", default="fallback")
        assert result == "fallback"

    def test_get_missing_section_returns_default(self, temp_config):
        from modules.Config import get_config

        result = get_config("nonexistent_section", "key", default="x")
        assert result == "x"

    def test_set_updates_existing_key(self, temp_config):
        from modules.Config import get_config, set_config

        set_config("ai", "provider", "openai")
        set_config("ai", "provider", "ollama")
        assert get_config("ai", "provider") == "ollama"

    def test_set_creates_new_section(self, temp_config):
        from modules.Config import get_config, set_config

        set_config("display", "style", "minimal")
        assert get_config("display", "style") == "minimal"

    def test_set_api_key(self, temp_config):
        from modules.Config import get_config, set_config

        set_config("ai", "api_key", "sk-test-key-12345")
        assert get_config("ai", "api_key") == "sk-test-key-12345"


# ──────────────────────────────────────────────────────────────────────────────
# show_config
# ──────────────────────────────────────────────────────────────────────────────


class TestShowConfig:
    def test_show_empty_config(self, runner, temp_config):
        from vocabCLI import app

        result = runner.invoke(app, ["config", "--show"])
        assert result.exit_code == 0

    def test_show_after_set(self, runner, temp_config):
        from modules.Config import set_config
        from vocabCLI import app

        set_config("ai", "provider", "openai")
        result = runner.invoke(app, ["config", "--show"])
        assert result.exit_code == 0
        assert "openai" in result.stdout


# ──────────────────────────────────────────────────────────────────────────────
# Database path override
# ──────────────────────────────────────────────────────────────────────────────


class TestDatabasePath:
    def test_env_var_overrides_default(self, tmp_path, monkeypatch):
        test_db = str(tmp_path / "test.db")
        monkeypatch.setenv("VOCABCLI_DB_PATH", test_db)
        from modules.Database import _get_db_path

        assert _get_db_path() == test_db

    def test_default_path_in_home(self, monkeypatch):
        monkeypatch.delenv("VOCABCLI_DB_PATH", raising=False)
        from modules.Database import _get_db_path

        path = _get_db_path()
        assert ".vocabcli" in path
        assert path.endswith("VocabularyBuilder.db")

    def test_creates_directory_if_missing(self, tmp_path, monkeypatch):
        new_dir = tmp_path / "new_vocabcli_dir"
        test_db = str(new_dir / "VocabularyBuilder.db")
        monkeypatch.setenv("VOCABCLI_DB_PATH", test_db)
        from modules.Database import _get_db_path, createConnection

        conn = createConnection()
        assert conn is not None
        conn.close()
