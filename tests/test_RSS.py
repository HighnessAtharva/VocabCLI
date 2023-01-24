from unittest import mock
import pytest
from vocabCLI import app
# TODO: @anay complete all the tests below this point 🔻


class TestRSS:
    # ADD FEEDS
    
    def test_add_feed(self, runner):
        result=runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/"])
        assert result.exit_code == 0
        assert "Title:" in result.stdout
        assert "Link:" in result.stdout
        assert "Summary:" in result.stdout
        

    def test_add_feed_invalid_URL(self, runner):
        result=runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/asdsadsad"])
        assert result.exit_code == 0
        assert "Feed not found ❌" in result.stdout

    def test_add_feed_already_exists(self, runner):
        result=runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/"])
        assert result.exit_code == 0
        assert "Feed already exists ✅" in result.stdout

    
    # DELETE FEEDS
    def test_remove_feed(self, runner):
        result=runner.invoke(app, ["rss", "--delete"], input="1") 
        assert result.exit_code == 0
        assert "deleted successfully" in result.stdout

    def test_remove_feed_empty(self, runner):
        result=runner.invoke(app, ["rss", "--delete"], input="1") 
        assert result.exit_code == 0
        assert "Feed does not exist ❌" in result.stdout

    def test_remove_feed_index_out_of_range(self, runner):
        # add a feed
        runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/"])
        result=runner.invoke(app, ["rss", "--delete"], input="4") # index out of range
        assert result.exit_code == 0
        assert "Invalid index, out of range ❌" in result.stdout

    def test_remove_feed_index_not_int(self, runner):
        result=runner.invoke(app, ["rss", "--delete"], input="NaN") # index out of range
        assert result.exit_code == 0
        assert "Index should be a number 🔢" in result.stdout

    # LIST FEEDS
    def test_get_feeds(self, runner):
        # add a feed
        runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/"])
        result=runner.invoke(app, ["rss", "-l",])
        assert result.exit_code == 0
        assert "Title" in result.stdout
        assert "Link" in result.stdout
        assert "Summary" in result.stdout
        assert "Date added" in result.stdout

    def test_get_feeds_empty(self, runner):
        runner.invoke(app, ["rss", "--delete"], input="1") # delete all feeds
        result=runner.invoke(app, ["rss", "-l",])
        assert result.exit_code == 0
        assert "No feeds added yet" in result.stdout




    # GET FEED ITEMS
    def test_get_feed_items(self, runner):
        # add a feed
        runner.invoke(app, ["rss", "-a", "https://www.tor.com/series/reading-the-wheel-of-time/feed/"])
        result=runner.invoke(app, ["rss", "--read", "wheel"])
        assert result.exit_code == 0
        assert "Title" in result.stdout
        assert "Published On" in result.stdout
        assert "Article Summary" in result.stdout

    def test_get_feed_items_non_existent_feed(self, runner):
        result=runner.invoke(app, ["rss", "--read", "sdsd"])
        assert result.exit_code == 0
        assert "This feed is not added to your list" in result.stdout
