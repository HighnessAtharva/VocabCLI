from unittest import mock

import pytest

from vocabCLI import app

# TODO: @anay complete all the tests below this point 🔻


class TestNLP:
    class TestReadability:
        def test_readability_text(self, runner):
            result = runner.invoke(
                app,
                [
                    "readability",
                    "A black hole is a region of spacetime where gravity is so strong that nothing, including light or other electromagnetic waves, has enough energy to escape its event horizon.[2] The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.[3][4] The boundary of no escape is called the event horizon. Although it has a great effect on the fate and circumstances of an object crossing it, it has no locally detectable features according to general relativity.[5] In many ways, a black hole acts like an ideal black body, as it reflects no light.[6][7] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is of the order of billionths of a kelvin for stellar black holes, making it essentially impossible to observe directly.",
                ],
            )
            assert result.exit_code == 0
            assert "Lexicon Count: 153" in result.stdout
            assert "Character Count (without spaces): 761" in result.stdout
            assert "Sentence Count: 7" in result.stdout
            assert "Words Per Sentence: 21.9" in result.stdout
            assert "Readability Index: 49.25" in result.stdout

        def test_readability_URL(self, runner):
            result = runner.invoke(
                app, ["readability", "https://en.wikipedia.org/wiki/Black_hole"]
            )
            assert result.exit_code == 0
            assert "Lexicon Count: 15531" in result.stdout
            assert "Character Count (without spaces): 82755" in result.stdout
            assert "Sentence Count: 1016" in result.stdout
            assert "Words Per Sentence: 15.3" in result.stdout
            assert "Readability Index: 55.95" in result.stdout

        def test_readability_URL_invalid(self, runner):
            result = runner.invoke(
                app, ["readability", "https://en.wikipedia.org/wiki/Black_hole_invalid"]
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout

    class Test_Extract_Difficult_Words:
        def test_extract_difficult_words_text(self, runner):
            result = runner.invoke(
                app,
                [
                    "hardwords",
                    "A black hole is a region of spacetime where gravity is so strong that nothing, including light or other electromagnetic waves, has enough energy to escape its event horizon.[2] The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.[3][4] The boundary of no escape is called the event horizon. Although it has a great effect on the fate and circumstances of an object crossing it, it has no locally detectable features according to general relativity.[5] In many ways, a black hole acts like an ideal black body, as it reflects no light.[6][7] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is of the order of billionths of a kelvin for stellar black holes, making it essentially impossible to observe directly.",
                ],
            )
            assert result.exit_code == 0
            assert "Processing text... 📃" in result.stdout
            assert "Content Length:" in result.stdout
            assert "electromagnetic" in result.stdout
            assert "spacetime" in result.stdout

        def test_extract_difficult_words_URL(self, runner):
            result = runner.invoke(
                app, ["hardwords", "https://en.wikipedia.org/wiki/Black_hole"]
            )
            assert result.exit_code == 0
            assert "URL detected 🌐" in result.stdout
            assert "Content Length:" in result.stdout
            assert "supersymmetric" in result.stdout
            assert "thermodynamics" in result.stdout
            assert "geodesic" in result.stdout

        def test_extract_difficult_words_URL_invalid(self, runner):
            result = runner.invoke(
                app, ["hardwords", "https://en.wikipedia.org/wiki/Black_hole_invalid"]
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout

    # TODO
    class Test_Sentiment_Analysis:
        def test_sentiment_analysis_text(self, runner):
            result = runner.invoke(
                app,
                [
                    "sentiment",
                    "A black hole is a region of spacetime where gravity is so strong that nothing, including light or other electromagnetic waves, has enough energy to escape its event horizon.[2] The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.[3][4] The boundary of no escape is called the event horizon. Although it has a great effect on the fate and circumstances of an object crossing it, it has no locally detectable features according to general relativity.[5] In many ways, a black hole acts like an ideal black body, as it reflects no light.[6][7] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is of the order of billionths of a kelvin for stellar black holes, making it essentially impossible to observe directly.",
                ],
            )
            assert result.exit_code == 0

        def test_sentiment_analysis_URL(self, runner):
            result = runner.invoke(
                app, ["sentiment", "https://en.wikipedia.org/wiki/Black_hole"]
            )
            assert result.exit_code == 0

        def test_sentiment_analysis_URL_invalid(self, runner):
            result = runner.invoke(
                app, ["sentiment", "https://en.wikipedia.org/wiki/Black_hole_invalid"]
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout

    class Test_Censor:
        def test_censor_text_strict(self, runner):
            result = runner.invoke(
                app,
                [
                    "clean",
                    "It is unclear whether the word has always been considered vulgar or, if not, when it first came to be used to describe (often in an extremely angry, hostile or belligerent manner) unpleasant circumstances or people in an intentionally offensive way, such as in the term motherfucker, one of its more common usages in some parts of the English-speaking world. Some English-speaking countries censor it on television and radio. Andrea Millwood Hargrave's 2000 study of the attitudes of the British public found that fuck was considered the third-most-severe profanity, and its derivative motherfucker second. Cunt was considered the most severe",
                    "--strict",
                ],
            )
            assert result.exit_code == 0
            assert "Processing text... 📃" in result.stdout
            assert "Offensive words censored: 4 😤" in result.stdout

        def test_censor_URL_strict(self, runner):
            result = runner.invoke(
                app, ["clean", "https://en.wikipedia.org/wiki/Fuck", "--strict"]
            )
            assert result.exit_code == 0
            assert "URL detected 🌐" in result.stdout
            assert "Offensive words censored: 152 😤" in result.stdout

        def test_censor_URL_strict_invalid(self, runner):
            result = runner.invoke(
                app,
                [
                    "clean",
                    "https://en.wikipedia.org/wiki/Black_hole_invalid",
                    "--strict",
                ],
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout

        def test_censor_text_no_strict(self, runner):
            result = runner.invoke(
                app,
                [
                    "clean",
                    "It is unclear whether the word has always been considered vulgar or, if not, when it first came to be used to describe (often in an extremely angry, hostile or belligerent manner) unpleasant circumstances or people in an intentionally offensive way, such as in the term motherfucker, one of its more common usages in some parts of the English-speaking world. Some English-speaking countries censor it on television and radio. Andrea Millwood Hargrave's 2000 study of the attitudes of the British public found that fuck was considered the third-most-severe profanity, and its derivative motherfucker second. Cunt was considered the most severe",
                ],
            )
            assert result.exit_code == 0
            assert "Processing text... 📃" in result.stdout
            assert "Offensive words censored: 4 😤" in result.stdout

        def test_censor_URL_no_strict(self, runner):
            result = runner.invoke(app, ["clean", "https://en.wikipedia.org/wiki/Fuck"])
            assert result.exit_code == 0
            assert "URL detected 🌐" in result.stdout
            assert "Offensive words censored: 152 😤" in result.stdout

        def test_censor_URL_no_strict_invalid(self, runner):
            result = runner.invoke(
                app, ["clean", "https://en.wikipedia.org/wiki/Black_hole_invalid"]
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout

    class Test_Summarize:
        def test_summarize_text(self, runner):
            result = runner.invoke(
                app,
                [
                    "summary",
                    "A black hole is a region of spacetime where gravity is so strong that nothing, including light or other electromagnetic waves, has enough energy to escape its event horizon.[2] The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.[3][4] The boundary of no escape is called the event horizon. Although it has a great effect on the fate and circumstances of an object crossing it, it has no locally detectable features according to general relativity.[5] In many ways, a black hole acts like an ideal black body, as it reflects no light.[6][7] Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is of the order of billionths of a kelvin for stellar black holes, making it essentially impossible to observe directly.",
                ],
            )
            assert result.exit_code == 0
            assert "Processing text... 📃" in result.stdout
            assert "Length of the article:" in result.stdout
            assert "Length of the summary:" in result.stdout
            assert "Summary:" in result.stdout

        def test_summarize_URL(self, runner):
            result = runner.invoke(
                app,
                [
                    "summary",
                    "https://www.teachermagazine.com/in_en/articles/using-toys-to-improve-learning",
                ],
            )
            assert result.exit_code == 0

            assert "URL detected 🌐" in result.stdout
            assert "Length of the article:" in result.stdout
            assert "Length of the summary:" in result.stdout
            assert "Summary:" in result.stdout

        def test_summarize_URL_invalid(self, runner):
            result = runner.invoke(
                app, ["summary", "https://en.wikipedia.org/wiki/Black_hole_invalid"]
            )
            assert result.exit_code == 0
            assert "The URL is not valid" in result.stdout
