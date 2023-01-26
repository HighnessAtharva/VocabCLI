""" HOW TO RUN TESTS """
# Run all Tests: ⏩ python -m pytest ../tests -vvv
# Run specific Class Test: ⏩ python -m pytest -k "ClassName" ../tests -vvv
# Run a specific Test: ⏩ python -m pytest -k "test_bye" ../tests -vvv

# NOTE:
# To tackle confirmation prompts, we are using the following approach: https://github.com/tiangolo/typer/issues/205
# @mock.patch("typer.confirm") and mock_typer_confirm.return_value = True/False are used to mock the confirmation prompt [Yes/No] respectively.

import os
import shutil
import sqlite3
from pathlib import Path

import pytest
from modules.Database import *
from modules.WordCollections import *
from typer.testing import CliRunner


def pytest_sessionstart(session):
    """
    Will run before any test.
    Setup any state specific to the execution.
    """

    if not os.path.exists("VocabularyBuilder.db"):
        return

    # move the app database to the parent directory
    app_DB_path = os.path.join(os.getcwd(), "VocabularyBuilder.db")
    parent_dir = Path(os.getcwd()).parents[0]
    shutil.move(app_DB_path, parent_dir)

    initializeDB()  # this is from Database.py
    insert_collection_to_DB()  # this is from WordCollections.py


def pytest_sessionfinish(session, exitstatus):
    """
    Will run after all tests.
    Teardown any state that was previously setup with a setup_module method.
    """

    # close the connection
    conn = sqlite3.connect("./VocabularyBuilder.db")
    conn.close()

    # delete the test database
    if os.path.exists("VocabularyBuilder.db"):
        os.remove("VocabularyBuilder.db")

    # move the app database back to the app folder
    app_DB_path = os.path.join(Path(os.getcwd()).parents[0], "VocabularyBuilder.db")
    current_dir = os.getcwd()
    shutil.move(app_DB_path, current_dir)


# This is a fixture that will be used in all tests, must be passed as an argument to the test function
@pytest.fixture(scope="session")
def runner():
    return CliRunner()
