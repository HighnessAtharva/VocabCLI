import pytest
from VocabularyCLI import app
from unittest import mock

# TODO: @anay complete all the tests below this point 🔻


class TestGraph:
    class Test_Top_Words_Bar_Graph:
        # top words bar graph
        def test_graph_bar_top_words(self, runner):
            pass

        def test_graph_bar_top_words_zero(self, runner):
            pass

        def test_graph_bar_top_words_less_than_N(self, runner):
            pass

    class Test_Top_Words_Pie_Chart:
        def top_words_pie_chart(self, runner):
            pass

        def top_words_pie_chart_zero(self, runner):
            pass

        def test_graph_top_words_less_than_N(self, runner):
            pass

    class Test_Top_Tags_Bar_Graph:
        def test_graph_top_tags_bar(self, runner):
            pass

        def test_graph_top_tags_bar_zero(self, runner):
            pass

        def test_graph_top_tags_bar_less_than_N(self, runner):
            pass

    class Test_Top_Tags_Pie_Chart:
        def test_graph_top_tags_pie(self, runner):
            pass

        def test_graph_top_tags_pie_zero(self, runner):
            pass

        def test_graph_top_tags_pie_less_than_N(self, runner):
            pass

    class Test_LearnVsMaster:
        def test_graph_learnVsMaster(self, runner):
            pass

        def test_graph_learnVsMaster_zero_both(self, runner):
            pass

        def test_graph_learnVsMaster_zero_learn(self, runner):
            pass

        def test_graph_learnVsMaster_zero_master(self, runner):
            pass

    class Test_Lookup_History:
        def test_graph_lookup_history_week(self, runner):
            pass

        def test_graph_lookup_history_month(self, runner):
            pass

        def test_graph_lookup_history_year(self, runner):
            pass

    class Test_Word_Category:
        def test_graph_word_category(self, runner):
            pass

        def test_graph_word_category_zero_words_in_DB(self, runner):
            pass
