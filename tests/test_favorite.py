from unittest import mock
import pytest
from VocabularyCLI import app


class TestFavorite:
    @mock.patch("typer.confirm")
    def test_favorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["favorite", "hello"])
        assert result.exit_code == 0
        assert "has been set as favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_favorite_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(app, ["favorite", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as favorite" in result.stdout
        assert "world has been set as favorite" in result.stdout

    def test_favorite_fake_word(self, runner):
        result = runner.invoke(app, ["favorite", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    @mock.patch("typer.confirm")
    def test_favorite_already_favorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["favorite", "hello"])
        result = runner.invoke(app, ["favorite", "hello"])
        assert result.exit_code == 0
        assert "is already marked as favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_unfavorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["favorite", "hello"])
        result = runner.invoke(app, ["unfavorite", "hello"])
        assert result.exit_code == 0
        assert "hello has been removed from favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_unfavorite_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "calm", "morning"])
        runner.invoke(app, ["favorite", "calm", "morning"])
        result = runner.invoke(app, ["unfavorite", "calm", "morning"])
        assert result.exit_code == 0
        assert "calm has been removed from favorite" in result.stdout
        assert "morning has been removed from favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_unfavorite_not_favorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["unfavorite", "hello"])
        assert result.exit_code == 0
        assert "was never favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_unfavorite_fake_word(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["unfavorite", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout
