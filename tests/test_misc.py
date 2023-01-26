from unittest import mock

import pytest

from vocabCLI import app


def test_bye(runner):
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "Bye bye!" in result.stdout


# TODO: Add tests for the about command


def test_about(runner):
    result = runner.invoke(app, ["about"])
    assert result.exit_code == 0
    assert "is a lightweight Command Line Interface" in result.stdout
    assert "Source:" in result.stdout
    assert "Dictionary and Thesaurus Lookups" in result.stdout
    assert "DONATIONS AND SUPPORT IS WELCOME" in result.stdout


def test_streak(runner):
    runner.invoke(app, ["define", "math", "school"])
    result = runner.invoke(app, ["streak"])
    assert result.exit_code == 0
    assert "Your longest word lookup streak is 1 day(s)" in result.stdout


@mock.patch("typer.confirm")
def test_streak_no_words(mock_typer, runner):
    runner.invoke(app, ["define", "math"])
    mock_typer.return_value = True
    runner.invoke(app, ["delete", "math"])
    runner.invoke(app, ["delete", "school"])
    result = runner.invoke(app, ["streak"])
    assert result.exit_code == 0
    assert (
        "There are no words in any of your lists. Add some words in your list using"
        in result.stdout
    )


def test_streak_multiple_days(runner):
    # TODO: HOW TO MOCK THE DATE?
    pass


@mock.patch("typer.confirm")
def test_milestone_no_words(mock_typer, runner):
    mock_typer.return_value = True
    runner.invoke(app, ["delete"])
    result = runner.invoke(app, ["milestone", "10"])
    assert result.exit_code == 0
    assert (
        "Cannot predict milestone as you have not looked up any words yet."
        in result.stdout
    )


def test_milestone_day_one(runner):
    runner.invoke(app, ["define", "math", "school"])
    result = runner.invoke(app, ["milestone", "10"])
    assert result.exit_code == 0
    assert "Keep learning words to get a prediction." in result.stdout


def test_milestone_day_two(runner):
    # TODO: HOW TO MOCK THE DATE?
    pass
    # runner.invoke(app, ["define", "math", "school"])
    # result=runner.invoke(app, ["milestone", "10"])
    # assert result.exit_code == 0
    # assert "You have been learning" in result.stdout
    # assert "You have learnt" in result.stdout
    # assert "Based on your current word lookup rate, you will reach 10" in result.stdout


def test_milestone_already_reached(runner):
    # TODO:  Causes zero division error due to average_words_per_day=learning_count/(datetime.datetime.now()-first_date).days
    result = runner.invoke(app, ["milestone", "2"])
    assert result.exit_code == 0
    assert "You have already reached 2 words" in result.stdout


def test_quote_of_the_day(runner):
    result = runner.invoke(app, ["daily-quote"])
    assert result.exit_code == 0
    assert "🌟 Quote:" in result.stdout


def test_word_of_the_day(runner):
    result = runner.invoke(app, ["daily-word"])
    assert result.exit_code == 0
    assert "WORD OF THE DAY" in result.stdout


def test_spell_checker(runner):
    result = runner.invoke(app, ["spellcheck", "kinder garden spfee"])
    assert result.exit_code == 0
    assert "kinder garden spfee" in result.stdout


def test_spell_checker_no_mispelling(runner):
    pass


def test_spell_checker_with_proper_nouns(runner):
    pass


def test_refresh_cache(runner):
    pass
