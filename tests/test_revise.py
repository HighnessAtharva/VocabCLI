from unittest import mock

import pytest

from vocabCLI import app


class TestRevise:
    class TestReviseDefault:
        @mock.patch("typer.confirm")
        def test_revise_default(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["revise"])
            assert result.exit_code == 0
            assert "Keep revising!" in result.stdout

        def test_revise_default_with_word_limit(self, runner):
            result = runner.invoke(app, ["revise", "-n", "2"])
            assert result.exit_code == 0
            assert "1 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_default_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["revise"])
            assert result.exit_code == 0
            assert "There are no words in any of your lists" in result.stdout

    class TestReviseTag:
        @mock.patch("typer.confirm")
        def test_revise_tag_correct(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            runner.invoke(
                app, ["tag", "math", "rock", "class", "gems", "--name", "diamonds"]
            )
            result = runner.invoke(app, ["revise", "--tag", "diamonds"])
            assert result.exit_code == 0
            assert "3 word(s) to go. Keep revising!" in result.stdout

        def test_revise_tag_incorrect(self, runner):
            result = runner.invoke(app, ["revise", "--tag", "faketag"])
            assert result.exit_code == 0
            assert "The tag faketag does not exist" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_tag_with_word_limit(self, mock_typer, runner):
            result = runner.invoke(app, ["revise", "--tag", "diamonds", "-n", "3"])
            assert result.exit_code == 0
            assert "2 word(s) to go. Keep revising!" in result.stdout

    class TestReviseMastered:
        @mock.patch("typer.confirm")
        def test_revise_mastered(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            runner.invoke(app, ["master", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["revise", "-m"])
            assert result.exit_code == 0
            assert "3 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_mastered_with_word_limit(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock"])
            runner.invoke(app, ["master", "math", "rock"])
            result = runner.invoke(app, ["revise", "-m", "-n", "2"])
            assert result.exit_code == 0
            assert "1 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_mastered_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["revise", "-m"])
            assert result.exit_code == 0
            assert "No words in your mastered list" in result.stdout

    class TestReviseLearning:
        @mock.patch("typer.confirm")
        def test_revise_learning(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            runner.invoke(app, ["learn", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["revise", "-l"])
            assert result.exit_code == 0
            assert "3 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_learning_with_word_limit(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            runner.invoke(app, ["learn", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["revise", "-l", "-n", "2"])
            assert result.exit_code == 0
            assert "1 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_learning_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["revise", "-l"])
            assert result.exit_code == 0
            assert "No words in your learning list" in result.stdout

    class TestReviseFavorite:
        @mock.patch("typer.confirm")
        def test_revise_favorite(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            runner.invoke(app, ["favorite", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["revise", "-f"])
            assert result.exit_code == 0
            assert "3 word(s) to go. Keep revising!" in result.stdout

        def test_revise_favorite_with_word_limit(self, runner):
            runner.invoke(app, ["favorite", "math", "rock"])
            result = runner.invoke(app, ["revise", "-f", "-n", "2"])
            assert result.exit_code == 0
            assert "1 word(s) to go. Keep revising!" in result.stdout

        @mock.patch("typer.confirm")
        def test_revise_favorite_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["revise", "-f"])
            assert result.exit_code == 0
            assert "No words in your favorite list" in result.stdout

    class TestReviseCollection:

        # this test runs the revise command for all the 500 words and takes a long time, find a way to break out of the loop
        # def test_revise_collection(self, runner):
        #     result= runner.invoke(app,["revise", "--collection", "500 SAT words"])
        #     assert result.exit_code == 0
        #     assert "499 word(s) to go. Keep revising!" in result.stdout
        # break out

        def test_revise_collection_with_word_limit(self, runner):
            result = runner.invoke(
                app, ["revise", "--collection", "500 SAT words", "-n", "3"]
            )
            assert result.exit_code == 0
            assert "2 word(s) to go. Keep revising!" in result.stdout

        def test_revise_fake_collection(self, runner):
            result = runner.invoke(app, ["revise", "--collection", "fakeCollection"])
            assert result.exit_code == 0
            assert "The collection fakeCollection is not available" in result.stdout
