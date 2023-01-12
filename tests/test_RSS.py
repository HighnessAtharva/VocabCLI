from unittest import mock
import pytest
from vocabCLI.__main__ import app
# TODO: @anay complete all the tests below this point 🔻


class TestRSS:
    class test_add_feed:
        def test_add_feed(self, runner):
            pass

        def test_add_feed_invalid_URL(self, runner):
            pass

        def test_add_feed_already_exists(self, runner):
            pass

    class test_get_feeds:
        def test_get_feeds(self, runner):
            pass

        def test_get_feeds_empty(self, runner):
            pass

    class test_remove_feed():
        def test_remove_feed(self, runner):
            pass

        def test_remove_feed_empty(self, runner):
            pass

        def test_remove_feed_index_out_of_range(self, runner):
            pass

        def test_remove_feed_index_not_int(self, runner):
            pass

    class test_get_feed_items():
        def test_get_feed_items(self, runner):
            pass

        def test_get_feed_items_non_existent_feed(self, runner):
            pass
