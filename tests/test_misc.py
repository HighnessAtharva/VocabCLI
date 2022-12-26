import pytest
from VocabularyCLI import app


def test_bye(runner):
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout

# TODO: Add tests for the about command


def test_about(runner):
    pass
