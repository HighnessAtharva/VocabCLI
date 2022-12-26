from unittest import mock
import pytest
from VocabularyCLI import app
from datetime import datetime


class TestList:
    def test_list_favorite(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["favorite", "math", "school"])
        result = runner.invoke(app, ["list", "-f"])
        assert result.exit_code == 0
        assert "Favorite [" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_favorite_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-f"])
        result = runner.invoke(app, ["list", "-f"])
        assert result.exit_code == 0
        assert "You have not added any words to the favorite list" in result.stdout

    def test_list_mastered(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["master", "math", "school"])
        result = runner.invoke(app, ["list", "-m"])
        assert result.exit_code == 0
        assert "Mastered [" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_mastered_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        result = runner.invoke(app, ["list", "-m"])
        assert result.exit_code == 0
        assert "You have not mastered any words" in result.stdout

    def test_list_learning(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["learn", "math", "school"])
        result = runner.invoke(app, ["list", "-l"])
        assert result.exit_code == 0
        assert "Learning [" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_learning_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-l"])
        result = runner.invoke(app, ["list", "-l"])
        assert result.exit_code == 0
        assert "You have not added any words to the learning list" in result.stdout

    def test_list_days(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["list", "-d", "1"])
        assert result.exit_code == 0
        assert "Words added to the vocabulary builder list from" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_days_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list", "-d", "1"])
        assert result.exit_code == 0
        assert "No records found within this date range" in result.stdout

    def test_list_days_negative(self, runner):
        result = runner.invoke(app, ["list", "-d", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_date(self, runner):
        runner.invoke(app, ["define", "world"])
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        # handling typer.prompt() input, need to pass in the input as a string
        result = runner.invoke(
            app, ["list", "--date"], input=f"{day}\n{month}\n{year}")
        assert result.exit_code == 0
        assert "Words added to the vocabulary builder list on" in result.stdout

    def test_list_date_nonexistent(self, runner):
        result = runner.invoke(app, ["list", "--date"], input="01\n01\n2002")
        assert result.exit_code == 0
        assert "No records found for" in result.stdout

    def test_list_date_outside_calendar_range(self, runner):
        result = runner.invoke(app, ["list", "--date"], input="20\n34\n2022")
        assert result.exit_code == 0
        assert "Date must fall within calendar range" in result.stdout

    def test_list_last(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["list", "-L", "2"])
        assert result.exit_code == 0
        assert "Last [2] words searched" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_last_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list", "-L", "2"])
        assert result.exit_code == 0
        assert "You haven't searched for any words yet" in result.stdout

    def test_list_last_negative(self, runner):
        result = runner.invoke(app, ["list", "-L", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_tag(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["tag", "math", "school", "--name", "testtag"])
        result = runner.invoke(app, ["list", "-t", "testtag"])
        assert result.exit_code == 0
        assert "Words with tag testtag [2 word(s)]" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_tag_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list", "-t", "testtag"])
        assert result.exit_code == 0
        assert "does not exist" in result.stdout

    def test_list_most(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["list", "-M", "2"])
        assert result.exit_code == 0
        assert "Top most searched words [2]" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_most_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list", "-M", "2"])
        assert result.exit_code == 0
        assert "You haven't searched for any words yet" in result.stdout

    def test_list_most_negative(self, runner):
        result = runner.invoke(app, ["list", "-M", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_tagnames(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["tag", "math", "--name", "testtag1"])
        runner.invoke(app, ["tag", "school", "--name", "testtag2"])
        result = runner.invoke(app, ["list", "-T"])
        assert result.exit_code == 0
        assert "YOUR TAGS :" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_tagnames_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list", "-T"])
        assert result.exit_code == 0
        assert "You haven't added any tags to your words yet" in result.stdout

    def test_list_all(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Here is your list of words" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_all_nonexistent(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "You have no words in your vocabulary builder list" in result.stdout

    def test_list_all_collection_names(self, runner):
        result = runner.invoke(app, ["list", "--collections"])
        assert result.exit_code == 0
        assert "1500 advanced words" and "music" in result.stdout

    def test_list_words_in_collection(self, runner):
        result = runner.invoke(app, ["list", "--collection", "music"])
        assert result.exit_code == 0
        assert "Words from the collection music" and "accordian" and "blues" in result.stdout

    def test_list_words_in_collection_nonexistent(self, runner):
        result = runner.invoke(app, ["list", "--collection", "fakeCollection"])
        assert result.exit_code == 0
        assert "The collection fakeCollection is not available" in result.stdout
