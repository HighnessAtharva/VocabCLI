from unittest import mock

import pytest

from vocabCLI import app


class TestThesaurus:
    def test_antonyms(self, runner):
        result = runner.invoke(app, ["antonym", "large", "wise"])
        assert result.exit_code == 0
        assert "Antonyms of large are" in result.stdout
        assert "small" in result.stdout
        assert "minuscule" in result.stdout
        assert "tiny" in result.stdout

        assert "Antonyms of wise are" in result.stdout
        assert "foolish" in result.stdout

    def test_synonyms(self, runner):
        result = runner.invoke(app, ["synonym", "large", "drink"])
        assert result.exit_code == 0
        assert "Synonyms of large are" in result.stdout
        assert "great" in result.stdout
        assert "huge" in result.stdout
        assert "giant" in result.stdout

        assert "Synonyms of drink are" in result.stdout
        assert "imbibe" in result.stdout
        assert "sip" in result.stdout
        assert "gulp" in result.stdout
