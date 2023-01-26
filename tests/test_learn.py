from unittest import mock

import pytest

from vocabCLI import app


class TestLearn:
    @mock.patch("typer.confirm")
    def test_learn(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "has been set as learning. Keep revising!" in result.stdout

    @mock.patch("typer.confirm")
    def test_learn_mastered(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["master", "hello"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "has been set as learning. Keep revising!" in result.stdout

    @mock.patch("typer.confirm")
    def test_learn_mastered_false(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["master", "hello"])
        mock_typer.return_value = False
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "OK, not moving hello to learning." in result.stdout

    @mock.patch("typer.confirm")
    def test_learn_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(app, ["learn", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as learning" in result.stdout
        assert "world has been set as learning" in result.stdout

    def test_learn_fake_word(self, runner):
        result = runner.invoke(app, ["learn", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    @mock.patch("typer.confirm")
    def test_learn_already_learn(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["learn", "hello"])
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "is already marked as learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_unlearn(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["learn", "hello"])
        result = runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "has been removed from learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_unlearn_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "white", "black"])
        runner.invoke(app, ["learn", "white", "black"])
        result = runner.invoke(app, ["unlearn", "white", "black"])
        assert result.exit_code == 0
        assert "white has been removed from learning" in result.stdout
        assert "black has been removed from learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_unlearn_not_learn(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "was never learning" in result.stdout

    def test_unlearn_fake_word(self, runner):
        result = runner.invoke(app, ["unlearn", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout
