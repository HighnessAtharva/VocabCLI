import pytest
from vocabCLI import app
from unittest import mock


def test_bye(runner):
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout

# TODO: Add tests for the about command


def test_about(runner):
    result=runner.invoke(app, ["about"])
    assert result.exit_code == 0
    assert "is a lightweight Command Line Interface" in result.stdout
    assert "Source:" in result.stdout
    assert "Dictionary and Thesaurus Lookups" in result.stdout
    assert "DONATIONS AND SUPPORT IS WELCOME" in result.stdout


def test_streak(runner):
    runner.invoke(app, ["define", "math", "school"])
    result=runner.invoke(app, ["streak"])
    assert result.exit_code == 0
    assert "Your longest word lookup streak is 1 day(s)" in result.stdout

@mock.patch("typer.confirm")
def test_streak_no_words(mock_typer, runner):
    runner.invoke(app, ["define", "math"])
    mock_typer.return_value = True
    runner.invoke(app, ["delete", "math"])
    runner.invoke(app, ["delete", "school"])
    result=runner.invoke(app, ["streak"])
    assert result.exit_code == 0
    assert "There are no words in any of your lists. Add some words in your list using" in result.stdout
    
def test_streak_multiple_days(runner):
    # TODO: HOW TO MOCK THE DATE?
    pass



def test_milestone(runner):
    pass

def test_milestone_no_words(runner):
    pass

def test_milestone_already_reached(runner):
    pass



def test_quote_of_the_day(runner):
    result=runner.invoke(app, ["daily-quote"])
    assert result.exit_code == 0
    assert "🌟 Quote:" in result.stdout

def test_word_of_the_day(runner):
    result=runner.invoke(app, ["daily-word"])
    assert result.exit_code == 0
    assert "WORD OF THE DAY" in result.stdout





def test_spell_checker(runner):
    result=runner.invoke(app, ["spellcheck", "kinder garden spfee"])
    assert result.exit_code == 0
    assert "kinder garden spfee" in result.stdout

def test_spell_checker_no_mispelling(runner):
    pass

def test_spell_checker_with_proper_nouns(runner):
    pass