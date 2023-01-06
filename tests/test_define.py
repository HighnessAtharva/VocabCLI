from unittest import mock
import pytest
from vocabCLI import app


class TestDefine:
    def test_define(self, runner):
        result = runner.invoke(app, ["define", "hello"])
        assert result.exit_code == 0
        assert "5. " in result.stdout

    def test_define_fake_word(self, runner):
        result = runner.invoke(app, ["define", "fakewordhaha"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_short(self, runner):
        result = runner.invoke(app, ["define", "hello", "--short"])
        assert result.exit_code == 0
        assert """"Hello!" or an equivalent greeting""" in result.stdout

    def test_define_short_fake_word(self, runner):
        result = runner.invoke(app, ["define", "fakewordhaha", "--short"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_pronounce(self, runner):
        result = runner.invoke(app, ["define", "hello", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio played""" in result.stdout

    def test_define_pronounce_fake_word(self, runner):
        result = runner.invoke(app, ["define", "fakewordhaha", "--pronounce"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_pronounce_unavailable(self, runner):
        result = runner.invoke(app, ["define", "extraordinary", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio Unavailable""" in result.stdout

    def test_define_multiple_real_words(self, runner):
        result = runner.invoke(app, ["define", "indigo", "paint"])
        assert result.exit_code == 0
        assert """Having a deep purplish-blue""" in result.stdout  # substr from def of first word
        assert """To direct a radar beam toward""" in result.stdout  # substr from def of second word

    def test_define_multiple_real_fake_words(self, runner):
        result = runner.invoke(app, ["define", "fakewordhaha", "paint"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout  # error msg for fake word
        assert """To direct a radar beam toward""" in result.stdout  # substr from def of second word
