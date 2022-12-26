from unittest import mock
import pytest
from VocabularyCLI import app


class TestMaster:
    @mock.patch("typer.confirm")
    def test_master(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "has been set as mastered. Good work!" in result.stdout

    @mock.patch("typer.confirm")
    def test_master_learning(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["learn", "hello"])
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "has been set as mastered. Good work!" in result.stdout
        result = runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "was never learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_master_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(app, ["master", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as mastered" in result.stdout
        assert "world has been set as mastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_unmaster_multiple_words(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["master", "hello", "world"])
        result = runner.invoke(app, ["unmaster", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as unmastered" in result.stdout
        assert "world has been set as unmastered" in result.stdout

    def test_master_fake_word(self, runner):
        result = runner.invoke(app, ["master", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    @mock.patch("typer.confirm")
    def test_master_already_master(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["master", "hello"])
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "hello is already marked as mastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_unmaster(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["master", "hello"])
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "hello has been set as unmastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_unmaster_not_master(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "hello was never mastered" in result.stdout

    def test_unmaster_fake_word(self, runner):
        result = runner.invoke(app, ["unmaster", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout
