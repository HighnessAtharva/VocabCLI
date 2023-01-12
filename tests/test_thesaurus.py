from unittest import mock
import pytest
from vocabCLI.__main__ import app


class TestThesaurus:
    def test_antonyms(self, runner):
        result = runner.invoke(app, ["antonym", "large", "wise"])
        assert result.exit_code == 0
        assert "Antonyms of large are" in result.stdout
        assert "Antonyms of wise are" in result.stdout

    def test_synonyms(self, runner):
        result = runner.invoke(app, ["synonym", "large", "drink"])
        assert result.exit_code == 0
        assert "Synonyms of large are" in result.stdout
        assert "Synonyms of drink are" in result.stdout
