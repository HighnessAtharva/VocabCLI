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


# tests for define command
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
