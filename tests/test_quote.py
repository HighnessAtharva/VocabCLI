from unittest import mock
import pytest
from vocabCLI.__main__ import app
# TODO: @anay complete all the tests below this point 🔻


class TestQuotes:
    class Test_Add_Quote:
        @mock.patch("typer.confirm")
        def test_add_quote_and_author(self, mock_typer, runner):
            mock_typer.return_value = True
            result = runner.invoke(
                app, ["quote", "--add"], input="Lorem ipsum\njohn doe")
            assert result.exit_code == 0
            assert "Quote: Lorem ipsum by john doe added to your list" in result.stdout

        @mock.patch("typer.confirm")
        def test_add_quote_no_author(self, mock_typer, runner):
            mock_typer.return_value = False  # no author
            result = runner.invoke(
                app, ["quote", "--add"], input="Lorem ipsum x2")
            assert result.exit_code == 0
            assert "Quote: Lorem ipsum x2 by - added to your list" in result.stdout

        @mock.patch("typer.confirm")
        def test_add_empty_quote(self, mock_typer, runner):
            mock_typer.return_value = False  # no author
            result = runner.invoke(
                app, ["quote", "--add"], input=" ")
            assert result.exit_code == 0
            assert " Quote cannot be empty. ❌" in result.stdout

        @mock.patch("typer.confirm")
        def test_add_quote_and_author_empty_author(self, mock_typer, runner):
            mock_typer.return_value = True
            result = runner.invoke(app, ["quote", "--add"], input="Lorem ipsum x3\n\" \"")
            assert result.exit_code == 0
            assert "Author cannot have only whitespaces. ❌" in result.stdout

        @mock.patch("typer.confirm")
        def test_add_quote_and_author_with_quote_strings(self, mock_typer, runner):
            mock_typer.return_value = True
            result = runner.invoke(app, ["quote", "--add"], input="\"hi there\"\n\"John Doe\"")
            assert result.exit_code == 0
            assert " Quote: hi there by John Doe added to your list" in result.stdout
 

    class Test_List_Quotes:
        def test_list_quotes(self, runner):
            result = runner.invoke(app, ["quote", "--list"])
            assert result.exit_code == 0
            assert "quotes saved. 📚" in result.stdout

        @mock.patch("typer.confirm")
        def test_list_quotes_empty(self, mock_typer, runner):
            mock_typer.return_value = True # confirm delete
            runner.invoke(app, ["quote", "-D"]) # delete all quotes
            result = runner.invoke(app, ["quote", "--list"])
            assert result.exit_code == 0
            assert "There are no quotes in your list. Add some quotes in your list" in result.stdout
            
        

    class Test_Delete_Quote:
        @mock.patch("typer.confirm")
        def test_delete_quote(self, mock_typer, runner):
            # adding quote 1
            mock_typer.return_value = False  # no author
            runner.invoke(app, ["quote", "--add"], input="Lorem ipsum x2")
            
            # adding quote 2
            mock_typer.return_value = True # set author
            runner.invoke(app, ["quote", "--add"], input="Lorem ipsum\njohn doe")
            
            result= runner.invoke(app, ["quote", "--delete"], input="1")
            assert result.exit_code == 0
            assert "Quote 1: Lorem ipsum deleted successfully" in result.stdout
            
            
            
        @mock.patch("typer.confirm")
        def test_delete_quote_empty(self, mock_typer, runner):
            mock_typer.return_value = True # confirm delete
            runner.invoke(app, ["quote", "-D"]) # delete all quotes
            result= runner.invoke(app, ["quote", "--delete"], input="1")
            assert result.exit_code == 0
            assert "There are no quotes in your list" in result.stdout
            
            
        @mock.patch("typer.confirm")
        def test_delete_quote_index_out_of_range(self, mock_typer, runner):
            # adding quote 1
            mock_typer.return_value = False  # no author
            runner.invoke(app, ["quote", "--add"], input="Lorem ipsum x2")
            
            # adding quote 2
            mock_typer.return_value = True # set author
            runner.invoke(app, ["quote", "--add"], input="Lorem ipsum\njohn doe")
            
            result= runner.invoke(app, ["quote", "--delete"], input="3")
            assert result.exit_code == 0
            assert "is out of range" in result.stdout
        
        
        @mock.patch("typer.confirm")
        def test_delete_quote_index_not_int(self, mock_typer, runner):
            result= runner.invoke(app, ["quote", "--delete"], input="NaN")
            assert result.exit_code == 0
            assert "is not a number" in result.stdout
        
        @mock.patch("typer.confirm")
        def test_delete_all_quotes(self, mock_typer, runner):
            mock_typer.return_value = True
            result = runner.invoke(app, ["quote", "-D"])
            assert result.exit_code == 0
            assert "All quotes deleted successfully" in result.stdout
        
        @mock.patch("typer.confirm")
        def test_delete_all_quotes_empty(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["quote", "-D"]) # delete all quotes to take care of previous tests
            mock_typer.return_value = True
            result=runner.invoke(app, ["quote", "-D"]) # delete all quotes again 
            assert result.exit_code == 0
            assert "There are no quotes in your list" in result.stdout

    # TODO: 
    class Test_Quote_Search:
        @mock.patch("typer.confirm")
        def test_quote_search(self, mock_typer, runner):
            pass

        @mock.patch("typer.confirm")    
        def test_quote_search_empty(self, mock_typer, runner):
            pass

        @mock.patch("typer.confirm")
        def test_quote_search_no_results(self, mock_typer, runner):
            pass

        @mock.patch("typer.confirm")
        def test_quote_search_empty_search(self, mock_typer, runner):
            pass

    @mock.patch("typer.confirm")
    def test_random_quote(self, mock_typer, runner):
        # delete all quotes
        mock_typer.return_value = True
        runner.invoke(app, ["quote", "-D"])
         
        # adding quote 1
        mock_typer.return_value = False  # no author
        runner.invoke(app, ["quote", "--add"], input="Lorem ipsum x2")

        result= runner.invoke(app, ["quote", "--random"])
        assert result.exit_code == 0
        assert "Lorem ipsum x2" in result.stdout
        
