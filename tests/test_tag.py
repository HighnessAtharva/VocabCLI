from unittest import mock
import pytest
from VocabularyCLI import app


class TestTag:
    @mock.patch("typer.confirm")
    def test_tag(self, mock_typer, runner):  # sourcery skip: class-extract-method
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["tag", "hello", "--name", "testtag"])
        assert result.exit_code == 0
        assert "has been tagged as" in result.stdout

    @mock.patch("typer.confirm")
    def test_tag_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(
            app, ["tag", "hello", "world", "--name", "testtag"])
        assert result.exit_code == 0
        assert "hello has been tagged as" in result.stdout
        assert "world has been tagged as" in result.stdout

    @mock.patch("typer.confirm")
    def test_untag_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        result = runner.invoke(app, ["untag", "hello", "world"])
        assert result.exit_code == 0
        assert "Tags deleted for the word hello" in result.stdout
        assert "Tags deleted for the word world" in result.stdout

    @mock.patch("typer.confirm")
    def test_tag_already_exists(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["tag", "hello", "--name", "testtag"])
        result = runner.invoke(app, ["tag", "hello", "--name", "testtag2"])
        assert result.exit_code == 0
        assert "has been changed to" in result.stdout

    def test_tag_fake_word(self, runner):
        result = runner.invoke(
            app, ["tag", "fakeworkhaha", "--name", "testtag"])
        # @atharva why is the exit code 0 here (and everywhere else where the word was not tagged) and not 1? We've wrote 1 in def test_untag_fake_word
        assert result.exit_code == 0
        assert "was never tracked before." in result.stdout

    @mock.patch("typer.confirm")
    def test_untag(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["tag", "hello", "--name", "testtag2"])
        result = runner.invoke(app, ["untag", "hello"])
        assert result.exit_code == 0
        assert "Tags deleted for the word" in result.stdout

    @mock.patch("typer.confirm")
    def test_untag_not_tagged(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["untag", "hello"])
        assert result.exit_code == 0
        assert "was not tagged" in result.stdout

    def test_untag_fake_word(self, runner):
        result = runner.invoke(app, ["untag", "fakewordhaha"])
        assert result.exit_code == 1  # exception raised
        assert "was never tracked before." in result.stdout
