import pytest
from vocabCLI import app
from unittest import mock


def test_bye(runner):
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout

# TODO: Add tests for the about command


def test_about(runner):
    pass


def test_streak(runner):
    pass


def test_milestone(runner):
    pass


def test_quote_of_the_day(runner):
    pass

def test_word_of_the_day(runner):
    pass