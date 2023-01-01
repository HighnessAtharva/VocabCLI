import pytest
from VocabularyCLI import app
from unittest import mock

# TODO: @anay complete all the tests below this point 🔻

# todo complete Graph Tests
# @atharva all the asserts are print panel statements, also no testing for export/popup?
# @anay Will do that a bit later, refer these links for testing plots
# - https://stackoverflow.com/questions/60127165/pytest-test-function-that-creates-plots
# - https://pypi.org/project/pytest-plt/


class TestGraph:
    class Test_Top_Words_Bar_Graph:
        @mock.patch("typer.confirm")
        def test_graph_bar_top_words(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class",
                          "math", "red", "colour", "traffic", "stuck", "happy"])
            result = runner.invoke(app, ["graph", "--topwordsbar", "5"])
            assert result.exit_code == 0
            assert "Displaying Bar graph of top 5" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_bar_top_words_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["graph", "--topwordsbar", "1"])
            assert result.exit_code == 0
            assert "No words found" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_bar_top_words_less_than_N(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "rock"])
            result = runner.invoke(app, ["graph", "--topwordsbar", "5"])
            assert result.exit_code == 0
            assert "Not enough words found. Showing graph for available words only" in result.stdout

    class Test_Top_Words_Pie_Chart:
        @mock.patch("typer.confirm")
        def top_words_pie_chart(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class",
                          "math", "red", "colour", "traffic", "stuck", "happy"])
            result = runner.invoke(app, ["graph", "--topwordspie"])
            assert result.exit_code == 0
            assert "Displaying Pie Chart of top" in result.stdout

        @mock.patch("typer.confirm")
        def top_words_pie_chart_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["graph", "--topwordspie"])
            assert result.exit_code == 0
            assert "No words found." in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_top_words_less_than_N(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "rock"])
            result = runner.invoke(app, ["graph", "--topwordspie"])
            assert result.exit_code == 0
            assert "Not enough words found" and "Pie" in result.stdout

    class Test_Top_Tags_Bar_Graph:
        @mock.patch("typer.confirm")
        def test_graph_top_tags_bar(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "red",
                          "colour", "traffic", "stuck", "happy", "sad", "rain"])
            runner.invoke(app, ["tag", "math", "--name", "testtag"])
            runner.invoke(app, ["tag", "rock", "--name", "testtag1"])
            runner.invoke(app, ["tag", "class", "--name", "testtag2"])
            runner.invoke(app, ["tag", "red", "--name", "testtag3"])
            runner.invoke(app, ["tag", "colour", "--name", "testtag4"])
            runner.invoke(app, ["tag", "traffic", "--name", "testtag5"])
            runner.invoke(app, ["tag", "stuck", "--name", "testtag6"])
            runner.invoke(app, ["tag", "happy", "--name", "testtag7"])
            runner.invoke(app, ["tag", "sad", "--name", "testtag8"])
            runner.invoke(app, ["tag", "rain", "--name", "testtag9"])
            result = runner.invoke(app, ["graph", "--toptagsbar", "9"])
            assert result.exit_code == 0
            assert "Displaying Bar graph of top" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_top_tags_bar_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["graph", "--toptagsbar", "10"])
            assert result.exit_code == 0
            assert "No tags found" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_top_tags_bar_less_than_N(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math"])
            runner.invoke(app, ["tag", "math", "--name", "testtag"])
            result = runner.invoke(app, ["graph", "--toptagsbar", "7"])
            assert result.exit_code == 0
            assert "Not enough tags found. Showing graph for available tags only." in result.stdout

    class Test_Top_Tags_Pie_Chart:
        @mock.patch("typer.confirm")
        def test_graph_top_tags_pie(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "red",
                          "colour", "traffic", "stuck", "happy", "sad", "rain"])
            runner.invoke(app, ["tag", "math", "--name", "testtag"])
            runner.invoke(app, ["tag", "rock", "--name", "testtag1"])
            runner.invoke(app, ["tag", "class", "--name", "testtag2"])
            runner.invoke(app, ["tag", "red", "--name", "testtag3"])
            runner.invoke(app, ["tag", "colour", "--name", "testtag4"])
            runner.invoke(app, ["tag", "traffic", "--name", "testtag5"])
            runner.invoke(app, ["tag", "stuck", "--name", "testtag6"])
            runner.invoke(app, ["tag", "happy", "--name", "testtag7"])
            runner.invoke(app, ["tag", "sad", "--name", "testtag8"])
            runner.invoke(app, ["tag", "rain", "--name", "testtag9"])
            result = runner.invoke(app, ["graph", "--toptagspie"])
            assert result.exit_code == 0
            assert "Displaying Pie Chart of top" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_top_tags_pie_zero(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            result = runner.invoke(app, ["graph", "--toptagspie"])
            assert result.exit_code == 0
            assert "No tags found" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_top_tags_pie_less_than_N(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math"])
            runner.invoke(app, ["tag", "math", "--name", "testtag"])
            result = runner.invoke(app, ["graph", "--toptagspie"])
            assert result.exit_code == 0
            assert "Not enough tags found. Showing Pie Chart for available tags only." in result.stdout

    class Test_LearnVsMaster:
        @mock.patch("typer.confirm")
        def test_graph_learnVsMaster(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "school", "colour"])
            runner.invoke(app, ["master", "school", "colour"])
            runner.invoke(app, ["learn", "math"])
            result = runner.invoke(app, ["graph", "--learnvsmaster"])
            assert result.exit_code == 0
            assert "Displaying Stacked Bar Graph of mastered vs learning words" in result.stdout

        # def test_graph_learnVsMaster_zero_both(self, mock_typer, runner):
        #     # @atharva found no diff condition for this one
        #     pass

        # def test_graph_learnVsMaster_zero_learn(self, mock_typer, runner):
        #     # @atharva found no diff condition for this one
        #     pass

        # def test_graph_learnVsMaster_zero_master(self, mock_typer, runner):
        #     # @atharva found no diff condition for this one
        #     pass

    class Test_Lookup_History:
        @mock.patch("typer.confirm")
        def test_graph_lookup_history_week(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math"])
            result = runner.invoke(app, ["graph", "--lookupweek"])
            assert result.exit_code == 0
            assert "Displaying Bar Graph of weekly word lookup distribution" in result.stdout

        @mock.patch("typer.confirm")
        def test_graph_lookup_history_month(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "music"])
            result = runner.invoke(app, ["graph", "--lookupmonth"])
            assert result.exit_code == 0
            assert "Displaying Bar Graph of monthly word lookup distribution" in result.stdout

        # @atharva function yet to be written

        @mock.patch("typer.confirm")
        def test_graph_lookup_history_year(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "school"])
            result = runner.invoke(app, ["graph", "--lookupyear"])
            assert result.exit_code == 0
            assert "Displaying Bar Graph of yearly word lookup distribution" in result.stdout

    class Test_Word_Category:
        @mock.patch("typer.confirm")
        def test_graph_word_category(self, mock_typer, runner):
            mock_typer.return_value = True
            runner.invoke(app, ["delete"])
            runner.invoke(app, ["define", "math", "rock", "class", "red",
                          "colour", "traffic", "stuck", "happy", "sad", "rain"])
            result = runner.invoke(app, ["graph", "--wordcategories"])
            assert result.exit_code == 0
            assert "Displaying Bar Graph of word distribution by category" in result.stdout

        # @mock.patch("typer.confirm")
        # def test_graph_word_category_zero_words_in_DB(self, mock_typer, runner):
        #     mock_typer.return_value = True
        #     runner.invoke(app, ["delete"])
        #     result = runner.invoke(app, ["graph", "--wordcategories"])
        #     # @atharva found no diff condition for this one
