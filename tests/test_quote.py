from unittest import mock
import pytest
from VocabularyCLI import app
# TODO: @anay complete all the tests below this point 🔻


class TestQuotes:
    class Test_Add_Quote:
        def test_add_quote_and_author(self, runner):
            pass

        def test_add_quote_no_author(self, runner):
            pass

        def test_add_quote_and_author_empty_quote(self, runner):
            pass

        def test_add_quote_and_author_empty_author(self, runner):
            pass

        def test_add_quote_and_author_empty_quote_and_author(self, runner):
            pass

        def test_add_quote_and_author_with_quotes(self, runner):
            pass

    class Test_List_Quotes:
        def test_list_quotes(self, runner):
            pass

        def test_list_quotes_empty(self, runner):
            pass

    class Test_Delete_Quotes:
        def test_delete_quotes(self, runner):
            pass

        def test_delete_quotes_empty(self, runner):
            pass

        def test_delete_quote_index_out_of_range(self, runner):
            pass

        def test_delete_quote_index_not_int(self, runner):
            pass

    class Test_Quote_Search:
        def test_quote_search(self, runner):
            pass

        def test_quote_search_empty(self, runner):
            pass

        def test_quote_search_no_results(self, runner):
            pass

        def test_quote_search_empty_search(self, runner):
            pass

    def test_random_quote(self, runner):
        pass
