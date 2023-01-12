from unittest import mock
import pytest
from vocabCLI.__main__ import app

# TODO: add tests for collection Quizzing


class TestQuiz:
    class TestQuizDefault:
        # @mock.patch("typer.confirm")
        # def test_quiz_default(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: gems" in result.stdout

        # @mock.patch("typer.confirm")
        # def test_quiz_default_with_word_limit(self,mock_typer, runner):
        #     # all words and word limit
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz","-n","4"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: gems" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_default_zero(self, mock_typer, runner):
            # zero words in DB
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["quiz"])
            assert result.exit_code == 0
            assert "There are no words in any of your lists" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_default_low_words(self, mock_typer, runner):
            # less than 4 words in DB
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math"])
            result = runner.invoke(app, ["quiz", "-n", "4"])
            assert result.exit_code == 0
            assert "Not enough words to start a quiz." in result.stdout

    class TestQuizTag:
        # @mock.patch("typer.confirm")
        # def test_quiz_tag_correct(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems","school", "interpret", "major",])
        #     runner.invoke(app, ["tag","math", "rock", "class", "school", "interpret", "major", "--name", "testtag"])
        #     result = runner.invoke(app,["quiz", "-t","testtag"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for class" in result.stdout

        # @mock.patch("typer.confirm")
        # def test_quiz_tag_with_word_limit(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     runner.invoke(app, ["tag","math", "rock", "class", "school", "--name", "testtag"])
        #     result = runner.invoke(app,["quiz", "-t","testtag", "-n", "4"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: rock" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_tag_incorrect(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "gems"])
            result = runner.invoke(app, ["quiz", "-t", "diamonds"])
            assert result.exit_code == 0
            assert "The tag diamonds does not exist" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_tag_low_words(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math"])
            runner.invoke(app, ["tag", "math", "--name", "diamonds"])
            result = runner.invoke(app, ["quiz", "-t", "diamonds", "-n", "4"])
            assert result.exit_code == 0
            assert "Not enough words to start a quiz." in result.stdout

    class TestQuizMastered:
        # @mock.patch("typer.confirm")
        # def test_quiz_mastered(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     runner.invoke(app, ["master","math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz", "-m"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: class" in result.stdout

        # @mock.patch("typer.confirm")
        # def test_quiz_mastered_with_word_limit(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     runner.invoke(app, ["master","math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz", "-m", "-n", "4"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: gems" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_mastered_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["quiz", "-m", "-n", "4"])
            assert result.exit_code == 0
            assert "No words in your mastered list" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_mastered_low_words(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class"])
            runner.invoke(app, ["master", "math", "rock", "class"])
            result = runner.invoke(app, ["quiz", "-m", "-n", "4"])
            assert result.exit_code == 0
            assert "Not enough words to start a quiz." in result.stdout

    class TestQuizLearning:
        # @mock.patch("typer.confirm")
        # def test_quiz_learning(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     runner.invoke(app, ["learn","math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz", "-l"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: gems" in result.stdout

        # @mock.patch("typer.confirm")
        # def test_quiz_learning_with_word_limit(self,mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     runner.invoke(app, ["define", "math", "rock", "class", "gems"])
        #     runner.invoke(app, ["learn","math", "rock", "class", "gems"])
        #     result = runner.invoke(app,["quiz", "-l", "-n", "4"])
        #     assert result.exit_code == 0
        #     assert "Choose the correct definition for: gems" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_learning_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["quiz", "-l", "-n", "4"])
            assert result.exit_code == 0
            assert "No words in your learning list" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_learning_low_words(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class"])
            runner.invoke(app, ["learn", "math", "rock", "class"])
            result = runner.invoke(app, ["quiz", "-l", "-n", "4"])
            assert result.exit_code == 0
            assert "Not enough words to start a quiz." in result.stdout

    class TestQuizFavorite:
        # @mock.patch("typer.confirm")
        # def test_quiz_favorite(self,mock_typer, runner):
        #     mock_typer.return_value = True

        # @mock.patch("typer.confirm")
        # def test_quiz_favorite_with_word_limit(self,mock_typer, runner):
        #     mock_typer.return_value = True

        @mock.patch("typer.confirm")
        def test_quiz_favorite_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["quiz", "-f"])
            assert result.exit_code == 0
            assert "No words in your favorite list" in result.stdout

        @mock.patch("typer.confirm")
        def test_quiz_favorite_low_words(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class"])
            runner.invoke(app, ["favorite", "math", "rock", "class"])
            result = runner.invoke(app, ["quiz", "-f", "-n", "4"])
            assert result.exit_code == 0
            assert "Not enough words to start a quiz." in result.stdout

    class TestQuizCollection:
        pass
        # @mock.patch("typer.confirm")
        # def test_quiz_collection(self,mock_typer, runner):
        #     mock_typer.return_value = True

        # @mock.patch("typer.confirm")
        # def test_quiz_collection_with_word_limit(self,mock_typer, runner):
        #     mock_typer.return_value = True

        def test_quiz_fake_collection(self, runner):
            result = runner.invoke(
                app, ["quiz", "--collection", "fakeCollection"])
            assert result.exit_code == 0
            assert "The collection fakeCollection is not available" in result.stdout
