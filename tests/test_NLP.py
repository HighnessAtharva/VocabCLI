import pytest
from VocabularyCLI import app
from unittest import mock

# TODO: @anay complete all the tests below this point 🔻


class TestNLP:
    class Test_Readability:
        def test_readability_text(self, runner):
            pass

        def test_readability_URL(self, runner):
            pass

        def test_readability_URL_invalid(self, runner):
            pass

    class Test_Extract_Difficult_Words:
        def test_extract_difficult_words_text(self, runner):
            pass

        def test_extract_difficult_words_URL(self, runner):
            pass

        def test_extract_difficult_words_URL_invalid(self, runner):
            pass

    class Test_Sentiment_Analysis:
        def test_sentiment_analysis_text(self, runner):
            pass

        def test_sentiment_analysis_URL(self, runner):
            pass

        def test_sentiment_analysis_URL_invalid(self, runner):
            pass

    class Test_Censor:
        def test_censor_text_strict(self, runner):
            pass

        def test_censor_URL_strict(self, runner):
            pass

        def test_censor_URL_strict_invalid(self, runner):
            pass

        def test_censor_text_no_strict(self, runner):
            pass

        def test_censor_URL_no_strict(self, runner):
            pass

    class Test_Summarize:
        def test_summarize_text(self, runner):
            pass

        def test_summarize_URL(self, runner):
            pass

        def test_summarize_URL_invalid(self, runner):
            pass
