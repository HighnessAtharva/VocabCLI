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
        assert """Could not find that word in the dictionary""" in result.stdout       

    def test_define_short(self):
        result = runner.invoke(app, ["define", "hello", "--short"])
        assert result.exit_code == 0
        assert """"Hello!" or an equivalent greeting""" in result.stdout
        
    def test_define_short_fake_word(self):
        result= runner.invoke(app, ["define", "fakewordhaha", "--short"])
        assert result.exit_code == 0
        assert """Could not find that word in the dictionary""" in result.stdout
        
    def test_define_pronounce(self):
        result= runner.invoke(app, ["define", "hello", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio played""" in result.stdout
        
    def test_define_pronounce_fake_word(self):
        result= runner.invoke(app, ["define", "fakewordhaha", "--pronounce"])
        assert result.exit_code == 0
        assert """Could not find that word in the dictionary""" in result.stdout
        
    def test_define_pronounce_unavailable(self):
        result= runner.invoke(app, ["define", "extraordinary", "--pronounce"])
        assert result.exit_code == 0
        assert """Audio Unavailable""" in result.stdout


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
        
        #should also be removed from learning if present, how to check it?
        
        #Solution -> 
        # You can make the runner invoke multiple commands in a single test case.

        # Once word is mastered, it will be removed from learning. So, we can check if it is present in learning list or not by using unlearn function and then asserting that it is not present in learning list. Because for unlearn function, if word is not present in learning list, it will print never learnt message.

        result=runner.invoke(app, ["unlearn", "hello"])
        assert result.exit_code == 0
        assert "was never learning" in result.stdout
        
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
      