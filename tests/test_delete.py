from unittest import mock
import pytest
from VocabularyCLI import app


class TestDelete:
    @mock.patch("typer.confirm")
    def test_delete(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello"])
        mock_typer.return_value = True  # mock the confirmation prompt [Y/N]->Y
        result = runner.invoke(app, ["delete", "hello"])
        assert result.exit_code == 0
        assert "hello deleted from your lists." in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_cancel_prompt(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello"])
        # mock the confirmation prompt [Y/N] -> N
        mock_typer.return_value = False
        result = runner.invoke(app, ["delete", "hello"])
        assert result.exit_code == 0
        assert "not deleting anything" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_multiple_words(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "world"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "hello", "world"])
        assert result.exit_code == 0
        assert "hello deleted from your lists." in result.stdout
        assert "world deleted from your lists." in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_unadded_word(self, mock_typer, runner):
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_master_word(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["master", "hello", "sky"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "--mastered"])
        assert result.exit_code == 0
        assert "All mastered words" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_empty_mastered(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "--mastered"])
        assert result.exit_code == 0
        assert "No words in your mastered list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_favorite_word(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["favorite", "hello", "sky"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "--favorite"])
        assert result.exit_code == 0
        assert "All favorite words" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_empty_favorite(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "-f"])
        assert result.exit_code == 0
        assert "No words in your favorite list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_learning_word(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["learn", "hello", "sky"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "-l"])
        assert result.exit_code == 0
        assert "All learning words" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_empty_learning(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "-l"])
        assert result.exit_code == 0
        assert "No words in your learning list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_tag(self, mock_typer, runner):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["tag", "hello", "sky", "--name", "soon"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "-t", "soon"])
        assert result.exit_code == 0
        assert " with tag soon deleted from your lists." in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_nonexistent_tag(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete", "-t", "soon"])
        assert result.exit_code == 0
        assert "The tag soon does not exist" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_all(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "sky"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete"])
        assert result.exit_code == 0
        assert "All words [2] deleted" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_no_words_exist(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        mock_typer.return_value = True
        result = runner.invoke(app, ["delete"])
        assert result.exit_code == 0
        assert "There are no words in any of your lists" in result.stdout
