""" HOW TO RUN TESTS """
# Run all Tests: ⏩ python -m pytest ../tests
# Run specific Class Test: ⏩ python -m pytest -k "ClassName" ../tests
# Run a specific Test: ⏩ python -m pytest -k "test_bye" ../tests



from typer.testing import CliRunner
from VocabularyBuilder import app
import pytest
  
runner=CliRunner()

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
        # adding this word to learning list programatically
        runner.invoke(app, ["define", "hello"])
        
        # reset learning value if it was already learning (edge case)
        runner.invoke(app, ["unlearn", "hello"])
        
        result = runner.invoke(app, ["learn", "hello"])
        assert result.exit_code == 0
        assert "has been set as learning. Keep revising!" in result.stdout
        
    def test_learn_multiple_words(self):
        pass
    
    def test_unlearn_multiple_words(self):
        pass

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
        assert "has been set as unlearning" in result.stdout
           
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
        pass

    def test_unmaster_multiple_words(self):
        pass
        
    def test_master_fake_word(self):
        result = runner.invoke(app, ["master", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout
        
    def test_master_already_master(self):
        result = runner.invoke(app, ["master", "hello"])
        assert result.exit_code == 0
        assert "is already marked as mastered" in result.stdout
        
    def test_unmaster(self):
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "has been set as unmastered" in result.stdout
           
    def test_unmaster_not_master(self):
        result = runner.invoke(app, ["unmaster", "hello"])
        assert result.exit_code == 0
        assert "was never mastered" in result.stdout
        
    def test_unmaster_fake_word(self):
        result = runner.invoke(app, ["unmaster", "fakewordhaha"])
        assert result.exit_code == 0
        assert "was never tracked before. Add some words" in result.stdout

class TestTag:    
    def test_tag(self):
        # adding this word to learning list programatically
        runner.invoke(app, ["delete", "hello"])
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["tag", "hello","--name", "testtag"])
        assert result.exit_code == 0
        assert "has been tagged as" in result.stdout
        
    def test_tag_already_exists(self):
        # adding this word to learning list programatically with a tag
        runner.invoke(app, ["define", "hello", "--tag", "testtag"])

        result = runner.invoke(app, ["tag", "hello", "--name", "testtag2"])
        assert result.exit_code == 0
        assert "tag has been changed to" in result.stdout
    
    def test_tag_fake_word(self):
        result=runner.invoke(app, ["tag", "fakeworkhaha", "--name", "testtag"])
        assert result.exit_code == 0 
        assert "is not a valid word" in result.stdout
        
    def test_untag(self):        
        # reset tag value if it was already tagged (edge case)
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["delete", "hello"])
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["tag", "hello", "--name", "testtag2"])

        result = runner.invoke(app, ["untag", "hello"])
        assert result.exit_code == 0
        assert "Tags deleted for the word" in result.stdout

    def test_untag_not_tagged(self):
        # reset tag value if it was already tagged (edge case)
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
        pass
    
    def test_delete_multiple_words(self):
        pass
    
    def test_delete_fake_word(self):
        pass
    
    def test_delete_unadded_word(self):
        pass
    
    
class TestList:
    pass