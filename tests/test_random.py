from unittest import mock
import pytest
from VocabularyCLI import app


class TestRandom:
    def test_random_word_api(self, runner):
        result = runner.invoke(app, ["random"])
        assert result.exit_code == 0
        assert "A Random Word for You:" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_master(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["master", "math", "school"])
        result = runner.invoke(app, ["random", "-m"])
        assert result.exit_code == 0
        assert "A Random word from your mastered words list: math" or "A Random word from your mastered words list: school" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_master_empty(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        result = runner.invoke(app, ["random", "-m"])
        assert result.exit_code == 0
        assert "No words in your mastered list" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_learning(self,  mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["learn", "math", "school"])
        result = runner.invoke(app, ["random", "-l"])
        assert result.exit_code == 0
        assert "A Random word from your learning words list: math" or "A Random word from your learning words list: school" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_learning_empty(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-l"])
        result = runner.invoke(app, ["random", "-l"])
        assert result.exit_code == 0
        assert "No words in your learning list" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_favorite(self,  mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["favorite", "math", "school"])
        result = runner.invoke(app, ["random", "-f"])
        assert result.exit_code == 0
        assert "A Random word from your favorite words list: math" or "A Random word from your favorite words list: school" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_favorite_empty(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-f"])
        result = runner.invoke(app, ["random", "-f"])
        assert result.exit_code == 0
        assert "No words in your favorite list" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_tag(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-t", "diamonds"])
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["tag", "math", "school", "--name", "diamonds"])
        result = runner.invoke(app, ["random", "-t", "diamonds"])
        assert result.exit_code == 0
        assert "A Random word from your diamonds tag: math" or "A Random word from your diamonds tag: school" in result.stdout

    @mock.patch("typer.confirm")
    def test_random_word_tag_empty(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-t", "diamonds"])
        result = runner.invoke(app, ["random", "-t", "diamonds"])
        assert result.exit_code == 0
        assert "The tag diamonds does not exist" in result.stdout

    def test_random_word_collection(self, runner):
        result = runner.invoke(app, ["random", "--collection", "music"])
        assert "A random word from the music collection" in result.stdout
