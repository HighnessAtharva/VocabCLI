from unittest import mock
import pytest
from vocabCLI import app
import os


class TestImportExport:
    def test_pdf_export(self, runner):
        runner.invoke(app, ["define", "hello"])
        result = runner.invoke(app, ["export", "--pdf"])
        assert result.exit_code == 0
        assert "WORDS TO PDF" in result.stdout
        # delete the created file
        test = os.listdir(os.getcwd())
        for item in test:
            if item.endswith(".pdf"):
                os.remove(os.path.join(os.getcwd(), item))

    # NOTE: This test will fail if there is a file named VocabularyWords.csv in the exports folder
    def test_csv_import_no_file(self, runner):
        result = runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "FILE NOT FOUND" in result.stdout

    def test_csv_import_with_duplicates(self, runner):
        runner.invoke(app, ["define", "hello"])
        runner.invoke(app, ["export"])
        result = runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "WITH THE SAME TIMESTAMP" in result.stdout

    @mock.patch("typer.confirm")
    def test_csv_import_without_duplicates(self, mock_typer, runner):
        runner.invoke(app, ["define", "math", "echo", "chamber"])
        runner.invoke(app, ["export"])
        mock_typer.return_value = True
        runner.invoke(app, ["delete"])
        result = runner.invoke(app, ["import"])
        assert result.exit_code == 0
        assert "IMPORTED" in result.stdout
