from unittest import mock

import pytest

from vocabCLI import app


class TestHistory:
    @mock.patch("typer.confirm")
    def test_history(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        runner.invoke(app, ["define", "math"])
        runner.invoke(app, ["define", "math", "rock"])
        result = runner.invoke(app, ["history", "math", "rock"])
        assert result.exit_code == 0
        assert "You have searched for math 2 time(s) before" in result.stdout
        assert "You have searched for rock 1 time(s) before" in result.stdout

    @mock.patch("typer.confirm")
    def test_history_never_added(self, mock_typer, runner):
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["history", "math"])
        assert result.exit_code == 0
        assert "The word math was never tracked before" in result.stdout
