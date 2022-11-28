""" HOW TO RUN TESTS """
# Run all Tests: ⏩ python -m pytest ../tests
# Run specific Class Test: ⏩ python -m pytest -k "ClassName" ../tests
# Run a specific Test: ⏩ python -m pytest -k "test_bye" ../tests

import pytest
import os
import shutil
from pathlib import Path
import sqlite3
from typer.testing import CliRunner
from VocabularyBuilder import app
 
runner=CliRunner()


def setup_module(module):
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
    c.execute(words)


def teardown_module(module):
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



# test for bye command
def test_bye():
    result = runner.invoke(app, ["bye"])
    assert result.exit_code == 0
    assert "👋 Bye bye!" in result.stdout


# test cases for define command
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
        # adding word to DB using define if it doesn't already exist
        runner.invoke(app, ["define", "hello"])

        # reset favorite value if it was already favorite (edge case)
        runner.invoke(app, ["unfavorite", "hello"])
                
        result = runner.invoke(app, ["favorite", "hello"])
        assert result.exit_code == 0
        assert "has been set as favorite" in result.stdout
        
    def test_favorite_multiple_words(self):
        # adding words to DB using define if it doesn't already exist
        runner.invoke(app, ["define", "hello", "world"])
        runner.invoke(app, ["unfavorite", "hello", "world"])
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


# test cases for master and unmaster commands
class TestMaster:    
    def test_master(self):    
        # adding this word to learning list programatically
        runner.invoke(app, ["define", "hello"])
        
        # reset master value if it was already master (edge case)
        runner.invoke(app, ["unmaster", "hello"])
        
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
        assert "is not a valid word" in result.stdout
        
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
        

class TestDelete:
    def test_delete(self):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["delete", "hello"])
        assert result.exit_code == 0 
        assert "hello deleted from your lists." in result.stdout
    
    def test_delete_multiple_words(self):
        runner.invoke(app, ["define", "hello", "world"])
        result = runner.invoke(app, ["delete", "hello", "world"])
        assert result.exit_code == 0 
        assert "hello deleted from your lists." in result.stdout
    
    
    def test_delete_unadded_word(self):
        runner.invoke(app, ["define", "fakewordhaha"])
        result = runner.invoke(app, ["delete", "fakewordhaha"])
        assert result.exit_code == 0 
        assert "was never tracked before" in result.stdout
        
    
class TestClear:
    def test_clear_all(self):
        runner.invoke(app, ["clear", "--all"])
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        result = runner.invoke(app, ["clear", "--all"])
        assert result.exit_code == 0 
        assert "All words[3] deleted" in result.stdout
    
    def test_clear_learning(self):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["learn", "hello", "world"])
        result = runner.invoke(app, ["clear", "--learning"])
        assert result.exit_code == 0 
        assert "All learning words[2] deleted" in result.stdout
    
    def test_clear_mastered(self):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["master", "hello", "world"])
        result = runner.invoke(app, ["clear", "--mastered"])
        assert result.exit_code == 0 
        assert "All mastered words[2] deleted" in result.stdout
    
    def test_clear_favorite(self):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["favorite", "hello", "world"])
        result = runner.invoke(app, ["clear", "--favorite"])
        assert result.exit_code == 0 
        assert "All favorite words[2] deleted" in result.stdout
    
    def test_clear_tag(self):
        runner.invoke(app, ["define", "hello", "world", "smash", "--short"])
        runner.invoke(app, ["tag", "hello", "world", "--name", "testtag"])
        result = runner.invoke(app, ["clear", "--tag", "testtag"])
        assert result.exit_code == 0 
        assert "All words[2] with tag testtag deleted" in result.stdout
    
    def test_clear_with_empty_db(self):
        runner.invoke(app, ["clear", "--all"])
        result = runner.invoke(app, ["clear", "--all"])
        assert result.exit_code == 0 
        assert "Nothing to delete." in result.stdout
        
    
    
 
class TestList:
    pass

class TestImportExport:
    def test_pdf_export(self):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["export", "--pdf"])
        assert result.exit_code == 0 
        assert "WORDS TO PDF" in result.stdout
          
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
        # programatically delete the csv file (if exists)
        test = os.listdir(os.getcwd())
        for item in test:
            if item.endswith(".csv"):
                os.remove(os.path.join(os.getcwd(), item))
        
        # try to import non-existent file
        result=runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "FILE NOT FOUND" in result.stdout