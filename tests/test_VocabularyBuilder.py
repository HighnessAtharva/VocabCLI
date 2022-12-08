""" HOW TO RUN TESTS """
# Run all Tests: ⏩ python -m pytest ../tests -vvv
# Run specific Class Test: ⏩ python -m pytest -k "ClassName" ../tests -vvv
# Run a specific Test: ⏩ python -m pytest -k "test_bye" ../tests -vvv

import os
import shutil
import sqlite3
from pathlib import Path
from unittest import mock

import pytest
from typer.testing import CliRunner
from VocabularyCLI import app

runner=CliRunner()


def setup_module():
    """
    Will run before any test.
    Setup any state specific to the execution.
    """

    if not os.path.exists("VocabularyBuilder.db"):
        return

    # move the app database to the parent directory
    app_DB_path=os.path.join(os.getcwd(), "VocabularyBuilder.db")
    parent_dir = Path(os.getcwd()).parents[0]
    shutil.move(app_DB_path, parent_dir)

    # create a test database
    conn = sqlite3.connect('./VocabularyBuilder.db')
    c = conn.cursor()
    words="""CREATE TABLE IF NOT EXISTS "words" (
        "word"	TEXT,
        "datetime"	timestamp NOT NULL UNIQUE,
        "tag"	TEXT,
        "mastered"	INTEGER NOT NULL DEFAULT 0,
        "learning"	INTEGER NOT NULL DEFAULT 0,
        "favorite"	INTEGER NOT NULL DEFAULT 0
    );
    """
    cache_words="""CREATE TABLE IF NOT EXISTS "cache_words" (
	"word"	TEXT NOT NULL UNIQUE,
    "api_response" json NOT NULL
);
    """

    c.execute(words)
    c.execute(cache_words)


def teardown_module():
    """
    Will run after all tests.
    Teardown any state that was previously setup with a setup_module method.
    """

    # close the connection
    conn = sqlite3.connect('./VocabularyBuilder.db')
    conn.close()

    # delete the test database
    if os.path.exists("VocabularyBuilder.db"):
        os.remove("VocabularyBuilder.db")

    # move the app database back to the app folder
    app_DB_path=os.path.join(Path(os.getcwd()).parents[0], "VocabularyBuilder.db")
    current_dir =  os.getcwd()
    shutil.move(app_DB_path, current_dir)


def test_bye():
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout


class TestDefine:
    def test_define(self):
        result = runner.invoke(app, ["define", "hello"])
        assert result.exit_code == 0
        assert "5. " in result.stdout

    def test_define_fake_word(self):
        result= runner.invoke(app, ["define", "fakewordhaha"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_short(self):
        result = runner.invoke(app, ["define", "hello", "--short"])
        assert result.exit_code == 0
        assert """"Hello!" or an equivalent greeting""" in result.stdout

    def test_define_short_fake_word(self):
        result= runner.invoke(app, ["define", "fakewordhaha", "--short"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_pronounce(self):
        result= runner.invoke(app, ["define", "hello", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio played""" in result.stdout

    def test_define_pronounce_fake_word(self):
        result= runner.invoke(app, ["define", "fakewordhaha", "--pronounce"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout

    def test_define_pronounce_unavailable(self):
        result= runner.invoke(app, ["define", "extraordinary", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio Unavailable""" in result.stdout

    def test_define_multiple_real_words(self):
        result= runner.invoke(app, ["define", "indigo", "paint"])
        assert result.exit_code == 0
        assert """Having a deep purplish-blue""" in result.stdout #substr from def of first word
        assert """To direct a radar beam toward""" in result.stdout #substr from def of second word

    def test_define_multiple_real_fake_words(self):
        result=runner.invoke(app, ["define","fakewordhaha", "paint"])
        assert result.exit_code == 0
        assert """is not a valid word""" in result.stdout #error msg for fake word
        assert """To direct a radar beam toward""" in result.stdout #substr from def of second word


# test cases for favorite and unfavorite commands
class TestFavorite:
    def test_favorite(self):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["favorite", "hello"])
        assert result.exit_code == 0
        assert "has been set as favorite" in result.stdout

    def test_favorite_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(app, ["unfavorite", "hello", "world"])
        result = runner.invoke(app, ["favorite", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as favorite" in result.stdout
        assert "world has been set as favorite" in result.stdout

    def test_unfavorite_multiple_words(self):
        runner.invoke(app, ["define", "calm", "morning"] )
        runner.invoke(app, ["favorite", "calm", "morning"])
        result = runner.invoke(app, ["unfavorite", "calm", "morning"])
        assert result.exit_code == 0
        assert "calm has been removed from favorite" in result.stdout
        assert "morning has been removed from favorite" in result.stdout

    def test_favorite_fake_word(self):
        result = runner.invoke(app, ["favorite", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    def test_favorite_already_favorite(self):
        result = runner.invoke(app, ["favorite", "hello"])
        assert result.exit_code == 0
        assert "is already marked as favorite" in result.stdout

    def test_unfavorite(self):
        result = runner.invoke(app, ["unfavorite", "hello"])
        assert result.exit_code == 0
        assert "has been removed from favorite" in result.stdout

    def test_unfavorite_not_favorite(self):
        result = runner.invoke(app, ["unfavorite", "hello"])
        assert result.exit_code == 0
        assert "was never favorite" in result.stdout


    def test_unfavorite_fake_word(self):
        result = runner.invoke(app, ["unfavorite", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout


# test cases for learn and unlearn commands
class TestLearn:
    def test_learn(self):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["unlearn", "hello"])
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "has been set as learning. Keep revising!" in result.stdout

    def test_learn_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["unlearn", "hello", "world"])
        result = runner.invoke(app, ["learn", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as learning" in result.stdout
        assert "world has been set as learning" in result.stdout

    def test_unlearn_multiple_words(self):
        runner.invoke(app, ["define", "white", "black"])
        runner.invoke(app, ["learn", "white", "black"])
        result = runner.invoke(app, ["unlearn", "white", "black"])
        assert result.exit_code == 0
        assert "white has been removed from learning" in result.stdout
        assert "black has been removed from learning" in result.stdout

    def test_learn_fake_word(self):
        result = runner.invoke(app, ["learn", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    def test_learn_already_learn(self):
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "is already marked as learning" in result.stdout

    def test_unlearn(self):
        result = runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "has been removed from learning" in result.stdout

    def test_unlearn_not_learn(self):
        result = runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "was never learning" in result.stdout


    def test_unlearn_fake_word(self):
        result = runner.invoke(app, ["unlearn", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout


class TestMaster:
    def test_master(self):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "has been set as mastered. Good work!" in result.stdout
        result=runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "was never learning" in result.stdout

    def test_master_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["learn", "hello", "world"])
        result = runner.invoke(app, ["master", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as mastered" in result.stdout
        assert "world has been set as mastered" in result.stdout

    def test_unmaster_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["master", "hello", "world"])
        result = runner.invoke(app, ["unmaster", "hello", "world"])
        assert result.exit_code == 0
        assert "hello has been set as learning" in result.stdout
        assert "world has been set as learning" in result.stdout

    def test_master_fake_word(self):
        result = runner.invoke(app, ["master", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

    def test_master_already_master(self):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["master", "hello"])
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "is already marked as mastered" in result.stdout

    def test_unmaster(self):
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "has been set as learning" in result.stdout

    def test_unmaster_not_master(self):
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "was never mastered" in result.stdout

    def test_unmaster_fake_word(self):
        result = runner.invoke(app, ["unmaster", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

class TestTag:
    def test_tag(self):  # sourcery skip: class-extract-method
        runner.invoke(app, ["delete", "hello"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["tag", "hello","--name", "testtag"])
        assert result.exit_code == 0
        assert "has been tagged as" in result.stdout

    def test_tag_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["untag", "hello", "world"])
        result=runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        assert result.exit_code == 0
        assert "hello has been tagged as" in result.stdout
        assert "world has been tagged as" in result.stdout


    def test_untag_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        result=runner.invoke(app, ["untag", "hello", "world"])
        assert result.exit_code == 0
        assert "Tags deleted for the word hello" in result.stdout
        assert "Tags deleted for the word world" in result.stdout

    def test_tag_already_exists(self):
        runner.invoke(app, ["tag", "hello", "--name", "testtag"])
        result = runner.invoke(app, ["tag", "hello", "--name", "testtag2"])
        assert result.exit_code == 0
        assert "tag has been changed to" in result.stdout

    def test_tag_fake_word(self):
        result=runner.invoke(app, ["tag", "fakeworkhaha", "--name", "testtag"])
        assert result.exit_code == 0
        assert "was never tracked before." in result.stdout

    def test_untag(self):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["delete", "hello"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["tag", "hello", "--name", "testtag2"])

        result = runner.invoke(app, ["untag", "hello"])
        assert result.exit_code == 0
        assert "Tags deleted for the word" in result.stdout

    def test_untag_not_tagged(self):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["untag", "hello"])
        result = runner.invoke(app, ["untag", "hello"])
        assert result.exit_code == 0
        assert "was not tagged" in result.stdout

    def test_untag_fake_word(self):
        result = runner.invoke(app, ["untag", "fakewordhaha"])
        assert result.exit_code == 1 # exception raised
        assert "was never tracked before." in result.stdout


# NOTE: To tackle confirmation prompts, we are using the following approach: https://github.com/tiangolo/typer/issues/205
# @mock.patch("typer.confirm") and mock_typer_confirm.return_value = True/False are used to mock the confirmation prompt [Yes/No] respectively.

class TestDelete:

    @mock.patch("typer.confirm")
    def test_delete(self, mock_typer):
        runner.invoke(app, ["define", "hello"])
        mock_typer.return_value = True # mock the confirmation prompt [Y/N]->Y
        result = runner.invoke(app, ["delete", "hello"])
        assert result.exit_code == 0
        assert "hello deleted from your lists." in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_cancel_prompt(self, mock_typer):
        runner.invoke(app, ["define", "hello"])
        mock_typer.return_value = False # mock the confirmation prompt [Y/N] -> N
        result = runner.invoke(app, ["delete", "hello"])
        assert result.exit_code == 0
        assert "not deleting anything" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_multiple_words(self, mock_typer):
        runner.invoke(app, ["define", "hello", "world"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "hello", "world"])
        assert result.exit_code == 0
        assert "hello deleted from your lists." in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_unadded_word(self, mock_typer):
        runner.invoke(app, ["define", "fakewordhaha"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_master_word(self, mock_typer):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["master", "hello", "sky"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "--mastered"])
        assert result.exit_code == 0
        assert "All mastered words [2] deleted" in result.stdout


    @mock.patch("typer.confirm")
    def test_delete_empty_mastered(self, mock_typer):
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "--mastered"])
        assert result.exit_code == 0
        assert "No words in your mastered list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_favorite_word(self, mock_typer):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["favorite", "hello", "sky"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "--favorite"])
        assert result.exit_code == 0
        assert "All favorite words [2] deleted" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_empty_favorite(self, mock_typer):
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "-f"])
        assert result.exit_code == 0
        assert "No words in your favorite list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_learning_word(self, mock_typer):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["learn", "hello", "sky"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "-l"])
        assert result.exit_code == 0
        assert "All learning words [2] deleted" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_empty_learning(self, mock_typer):
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "-l"])
        assert result.exit_code == 0
        assert "No words in your learning list" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_tag(self, mock_typer):
        runner.invoke(app, ["define", "hello", "sky"])
        runner.invoke(app, ["tag", "hello", "sky","--name", "soon" ])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "-t", "soon"])
        assert result.exit_code == 0
        assert "All words [2] with tag soon" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_nonexistent_tag(self, mock_typer):
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete", "-t", "soon"])
        assert result.exit_code == 0
        assert "No words in tag soon" in result.stdout

    @mock.patch("typer.confirm")
    def test_delete_all(self, mock_typer):
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "hello", "sky"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete"])
        assert result.exit_code == 0
        assert "All words [2] deleted" in result.stdout


    @mock.patch("typer.confirm")
    def test_delete_no_words_exist(self, mock_typer):
        mock_typer.return_value = True 
        result = runner.invoke(app, ["delete"])
        assert result.exit_code == 0
        assert "Nothing to delete" in result.stdout

class TestClear:

    @mock.patch("typer.confirm")
    def test_clear_learning(self, mock_typer):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["learn", "hello", "world"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "--learning"])
        assert result.exit_code == 0
        assert "All words have been removed from learning" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_mastered(self, mock_typer):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["master", "hello", "world"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "--mastered"])
        assert result.exit_code == 0
        assert "All words have been removed from mastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_favorite(self, mock_typer):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["favorite", "hello", "world"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "--favorite"])
        assert result.exit_code == 0
        assert "All words have been removed from favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_tag(self, mock_typer):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "--tag", "testtag"])
        assert result.exit_code == 0
        assert "All words have been removed from the tag testtag" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_favorites_with_no_favorites(self, mock_typer):
        mock_typer.return_value = True 
        runner.invoke(app, ["clear", "-f"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "-f"])
        assert result.exit_code == 0
        assert "No words are marked as favorite" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_mastered_with_no_mastered(self, mock_typer):
        mock_typer.return_value = True 
        runner.invoke(app, ["clear", "-m"])
        mock_typer.return_value = True 
        result = runner.invoke(app, ["clear", "-m"])
        assert result.exit_code == 0
        assert "No words are marked as mastered" in result.stdout

    @mock.patch("typer.confirm")
    def test_clear_tag_with_no_tagged_words(self, mock_typer):
        mock_typer.return_value = True 
        runner.invoke(app, ["clear", "-t", "testtag"])
        mock_typer.return_value = True 
        result=runner.invoke(app, ["clear", "-t", "testtag"])
        assert result.exit_code == 0
        assert "No words with the tag testtag were found" in result.stdout



class TestImportExport:
    def test_pdf_export(self):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["export", "--pdf"])
        assert result.exit_code == 0
        assert "WORDS TO PDF" in result.stdout
        # delete the created file
        test = os.listdir(os.getcwd())
        for item in test:
            if item.endswith(".pdf"):
                os.remove(os.path.join(os.getcwd(), item))

    def test_csv_import_with_duplicates(self):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["export"])
        result = runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "WITH THE SAME TIMESTAMP" in result.stdout

    # WARNING: Running this test will delete all the words in the database. Might want to comment it out.
    def test_csv_import_without_duplicates(self):
        runner.invoke(app, ["define", "math","echo", "chamber"])
        runner.invoke(app, ["export"])
        runner.invoke(app, ["clear", "--all"])
        result = runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "IMPORTED" in result.stdout

    def test_csv_import_no_file(self):
        # programmatically delete the csv file (if exists)
        test = os.listdir(os.getcwd())
        for item in test:
            if item.endswith(".csv"):
                os.remove(os.path.join(os.getcwd(), item))

        # try to import non-existent file
        result=runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "FILE NOT FOUND" in result.stdout



class TestThesaurus:
    def test_antonyms(self):
        result= runner.invoke(app, ["antonym", "large", "wise"])
        assert result.exit_code == 0
        assert "Antonyms of large are" in result.stdout
        assert "Antonyms of wise are" in result.stdout

    def test_synonyms(self):
        result= runner.invoke(app, ["synonym", "large", "drink"])
        assert result.exit_code == 0
        assert "Synonyms of large are" in result.stdout
        assert "Synonyms of drink are" in result.stdout


class TestList:
    def test_list_favorite(self):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["favorite", "math", "school"])
        result= runner.invoke(app, ["list", "-f"])
        assert result.exit_code == 0
        assert "Favorite words" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_favorite_nonexistent(self, mock_typer):
        runner.invoke(app, ["clear", "-f"])
        mock_typer.return_value = True
        result= runner.invoke(app, ["list", "-f"])
        assert result.exit_code == 0
        assert "You have not added any words to the favorite list" in result.stdout

    def test_list_mastered(self):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["master", "math", "school"])
        result= runner.invoke(app, ["list", "-m"])
        assert result.exit_code == 0
        assert "Mastered words" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_mastered_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-m"])
        result= runner.invoke(app, ["list", "-m"])
        assert result.exit_code == 0
        assert "You have not mastered any words" in result.stdout

    def test_list_learning(self):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["learn", "math", "school"])
        result= runner.invoke(app, ["list", "-l"])
        assert result.exit_code == 0
        assert "Learning words" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_learning_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["clear", "-l"])
        result= runner.invoke(app, ["list", "-l"])
        assert result.exit_code == 0
        assert "You have not added any words to the learning list" in result.stdout

    def test_list_days(self):
        runner.invoke(app, ["define", "math", "school"])
        result= runner.invoke(app, ["list", "-d", "1"])
        assert result.exit_code == 0
        assert "Words added to the vocabulary builder list from" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_days_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list", "-d", "1"])
        assert result.exit_code == 0
        assert "No records found within this date range" in result.stdout


    def test_list_days_negative(self):
        result= runner.invoke(app, ["list", "-d", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_date(self):
        runner.invoke(app, ["define", "world"])
        day= datetime.now().day
        month= datetime.now().month
        year= datetime.now().year
        
        result= runner.invoke(app, ["list", "--date"], input=f"{day}\n{month}\n{year}")
        assert result.exit_code == 0
        assert "Words added to the vocabulary builder list on" in result.stdout
        pass

    def test_list_date_nonexistent(self):
        result= runner.invoke(app, ["list", "--date"], input="2022\n12\n01")
        assert result.exit_code == 0
        assert "No records found on this date" in result.stdout

    # def test_list_date_invalid(self):
    #     result= runner.invoke(app, ["list", "-d", "efewq"])
    #     assert result.exit_code == 0
    #     assert "Please enter a valid date" in result.stdout

    def test_list_last(self):
        runner.invoke(app, ["define", "math", "school"])
        result= runner.invoke(app, ["list", "-L", "2"])
        assert result.exit_code == 0
        assert "Last [2] words searched" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_last_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list", "-L", "2"])
        assert result.exit_code == 0
        assert "You haven't searched for any words yet" in result.stdout

    def test_list_last_negative(self):
        result= runner.invoke(app, ["list", "-L", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_tag(self):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["tag", "math", "school", "--name", "testtag"])
        result= runner.invoke(app, ["list", "-t", "testtag"])
        assert result.exit_code == 0
        assert "Words with tag testtag [2 word(s)]" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_tag_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list", "-t", "testtag"])
        assert result.exit_code == 0
        assert "does not exist" in result.stdout

    def test_list_most(self):
        runner.invoke(app, ["define", "math", "school"])
        result= runner.invoke(app, ["list", "-M", "2"])
        assert result.exit_code == 0
        assert "Top most searched words [2]" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_most_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list", "-M", "2"])
        assert result.exit_code == 0
        assert "You haven't searched for any words yet" in result.stdout

    def test_list_most_negative(self):
        result= runner.invoke(app, ["list", "-M", "-1"])
        assert result.exit_code == 0
        assert "Enter a positive number" in result.stdout

    def test_list_tagnames(self):
        runner.invoke(app, ["define", "math", "school"])
        runner.invoke(app, ["tag", "math", "--name", "testtag1"])
        runner.invoke(app, ["tag", "school", "--name", "testtag2"])
        result= runner.invoke(app, ["list", "-T"])
        assert result.exit_code == 0
        assert "YOUR TAGS :" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_tagnames_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list", "-T"])
        assert result.exit_code == 0
        assert "You haven't added any tags to your words yet" in result.stdout

    def test_list_all(self):
        runner.invoke(app, ["define", "math", "school"])
        result= runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Here is your list of words" in result.stdout

    @mock.patch("typer.confirm")
    def test_list_all_nonexistent(self, mock_typer):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result= runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "You have no words in your vocabulary builder list" in result.stdout




class TestRate:
    pass
