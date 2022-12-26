from unittest import mock
import pytest
from VocabularyCLI import app


class TestClear:
    @mock.patch("typer.confirm")
    def test_clear_learning(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["learn", "hello", "world"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "--learning"])
        assert result.exit_code == 0
        assert "All words have been removed from learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_mastered(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["master", "hello", "world"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "--mastered"])
        assert result.exit_code == 0
        assert "All words have been removed from mastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_favorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["favorite", "hello", "world"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "--favorite"])
        assert result.exit_code == 0
        assert "All words have been removed from favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_tag(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "--tag", "testtag"])
        assert result.exit_code == 0
        assert "All words have been removed from the tag testtag" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_learning_with_no_learning(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-l"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "-l"])
        assert result.exit_code == 0
        assert "No words in your learning list" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_favorites_with_no_favorites(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-f"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "-f"])
        assert result.exit_code == 0
        assert "No words in your favorite list" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_mastered_with_no_mastered(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "-m"])
        assert result.exit_code == 0
        assert "No words in your mastered list" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_tag_with_no_tagged_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-t", "testtag"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["clear", "-t", "testtag"])
        assert result.exit_code == 0
        assert "The tag testtag does not exist" in result.stdout
