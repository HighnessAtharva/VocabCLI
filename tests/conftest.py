""" HOW TO RUN TESTS """
# Run all Tests (from repo root): ⏩ pytest
# Run specific Class Test: ⏩ pytest -k "ClassName" -vvv
# Run a specific Test: ⏩ pytest -k "test_bye" -vvv

# NOTE:
# To tackle confirmation prompts, we are using the following approach: https://github.com/tiangolo/typer/issues/205
# @mock.patch("typer.confirm") and mock_typer_confirm.return_value = True/False are used to mock the confirmation prompt [Yes/No] respectively.

import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

# Point the app to a temporary test database so tests never touch the user's
# real ~/.vocabcli/VocabularyBuilder.db.
_TEST_DB_DIR = tempfile.mkdtemp(prefix="vocabcli_test_")
_TEST_DB_PATH = os.path.join(_TEST_DB_DIR, "VocabularyBuilder_test.db")
os.environ.setdefault("VOCABCLI_DB_PATH", _TEST_DB_PATH)

from modules.Database import initializeDB  # noqa: E402 (after env var is set)
from modules.WordCollections import insert_collection_to_DB  # noqa: E402


def pytest_sessionstart(session):
    """Setup: initialise a fresh test database before any test runs."""
    initializeDB()
    insert_collection_to_DB()


def pytest_sessionfinish(session, exitstatus):
    """Teardown: remove the temporary test database after all tests finish."""
    try:
        if os.path.exists(_TEST_DB_PATH):
            os.remove(_TEST_DB_PATH)
        shutil.rmtree(_TEST_DB_DIR, ignore_errors=True)
    except Exception:
        pass


# This fixture is used by every test file that invokes CLI commands.
@pytest.fixture(scope="session")
def runner():
    return CliRunner()
