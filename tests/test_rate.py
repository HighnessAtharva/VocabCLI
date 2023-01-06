from unittest import mock
import pytest
from vocabCLI import app


class TestRate:
    def test_rate_default(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["rate"])
        assert result.exit_code == 0
        assert "words today compared to yesterday" in result.stdout

    def test_rate_today(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["rate", "-t"])
        assert result.exit_code == 0
        assert "words today compared to yesterday" in result.stdout

    def test_rate_week(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["rate", "-w"])
        assert result.exit_code == 0
        assert "words this week compared to last week" in result.stdout

    def test_rate_month(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["rate", "-m"])
        assert result.exit_code == 0
        assert "words this month compared to last month" in result.stdout

    def test_rate_year(self, runner):
        runner.invoke(app, ["define", "math", "school"])
        result = runner.invoke(app, ["rate", "-y"])
        assert result.exit_code == 0
        assert "words this year compared to last year" in result.stdout
