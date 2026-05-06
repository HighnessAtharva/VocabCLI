import os
from collections import Counter
from heapq import nlargest
from pathlib import Path
from string import punctuation
from typing import Optional, List

import nltk
import pandas as pd
import regex as re
import requests
import rich
import textstat
import trafilatura
from bs4 import BeautifulSoup
from rich import box, print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# NLP / ML dependencies are optional ([nlp] extra).  Degrade gracefully so
# that users who install only the core package don't get an ImportError.
try:
    import spacy
    import torch
    from spacy.lang.en.stop_words import STOP_WORDS
    from spacytextblob.spacytextblob import SpacyTextBlob
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    from spacy.cli import download as _spacy_download

    # Download the spaCy model on first use if not already present
    if not spacy.util.is_package("en_core_web_sm"):
        _spacy_download("en_core_web_sm")

    _NLP_AVAILABLE = True
except ImportError:
    _NLP_AVAILABLE = False
    STOP_WORDS: set = set()  # type: ignore[assignment]

_MODULES_DIR = Path(__file__).parent

_NLP_MISSING_PANEL = Panel(
    title="[b reverse yellow]  NLP Dependencies Missing  [/b reverse yellow]",
    title_align="center",
    padding=(1, 1),
    renderable=(
        "This feature requires the [bold cyan]nlp[/bold cyan] optional extras.\n\n"
        "Install with: [bold white]pip install \"vocabcli[nlp]\"[/bold white]"
    ),
)


def _require_nlp() -> bool:
    """Return True if NLP deps are available; print an error and return False otherwise.

    Returns:
        bool: True when spaCy, torch, and transformers are importable.
    """
    if not _NLP_AVAILABLE:
        print(_NLP_MISSING_PANEL)
        return False
    return True


URL_INVALID_PANEL = Panel(
    title="[b reverse red]  Error!  [/b reverse red]",
    title_align="center",
    padding=(1, 1),
    renderable="The URL is [bold red]not valid[/bold red] or the website is [bold red]not accessible.[/bold red] Please try again later. 😕",
)


# TODO: @atharva - add proper response headers and browser details to prevent false IP blocks.


def check_url_or_text(value: str) -> bool:
    """
    Checks if the value is a URL or a text

    1. Try to get the response from the URL, if we get a response, then it is a URL
    2. If we get an exception, then it is a text

    Args:
        value (str): URL or text to be checked

    Returns:
        bool: True if the value is a URL, False if the value is a text

    Raises:
        requests.exceptions.MissingSchema: If the URL is missing the schema
        requests.exceptions.InvalidSchema: If the URL has an invalid schema
        requests.exceptions.InvalidURL: If the URL is invalid
    """

    try:
        response = requests.get(value)
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.InvalidSchema:
        return False
    except requests.exceptions.InvalidURL:
        return False

    else:
        return True


def parse_text_from_web(webURL: str) -> str:
    """
    Extracts the text from the main content of the web page. Removes the ads, comments, navigation bar, footer, html tags, etc

    1. Download the web page using trafilatura
    2. Extract the text from the downloaded web page using trafilatura
    3. Return the extracted text

    Args:
        webURL (str): URL of the web page

    Returns:
        str: clean text from the web page

    Raises:
        trafilatura.errors.FetchingError: If the URL is invalid or the server is down
    """

    response = requests.get(webURL)
    if response.status_code != 200:
        return -1
    downloaded = trafilatura.fetch_url(webURL)
    return trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        with_metadata=False,
        include_formatting=True,
        target_language="en",
        include_images=False,
    )


def cleanup_text(text: str) -> str:
    """
    Clean up the text by removing special characters, numbers, whitespaces, etc for further processing and to improve the accuracy of the model.

    1. Remove the non-ascii characters
    2. Remove the numbers
    3. Remove the whitespaces
    4. Remove the special characters except full stop and apostrophe
    5. Convert the text to lowercase
    6. Remove the leading and trailing whitespaces
    7. Split the text into words without messing up the punctuation

    Args:
        text (str): text to be cleaned up

    Returns:
        str: cleaned up text
    """

    text = re.sub("\xc2\xa0", "", text)  # Deal with some weird tokens
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = re.sub(r"\s+", " ", text)  # remove whitespaces
    # remove special characters except full stop and apostrophe
    text = re.sub(r"[^a-zA-Z0-9\s.']", "", text)
    # text = text.lower()  # convert text to lowercase
    text = text.strip()  # remove leading and trailing whitespaces
    text = text.encode("ascii", "ignore").decode("ascii")  # remove non-ascii characters

    # split text into words without messing up the punctuation
    text = re.findall(r"[\w']+|[.,!?;]", text)

    return text


def censor_bad_words_strict(text: str) -> None:
    """
    Removes the bad words from the text and replaces them with asterisks completely and prints the censor text

    1. First we check if the text is a URL, if yes, then we parse the text from it and then use the model
    2. If the text is not a URL, then we directly use the model
    3. Remove the punctuations and convert text to lowercase
    4. Read the bad words from the file and store them in a list
    5. Split the text into words and for each word, we check if it is a bad word, if yes, then we replace it with asterisks
    6. Print the censored text and the number of bad words censored

    Args:
        text (str): text that needs to be censored
    """
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="monkey", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Censoring...", total=None)
        # ----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )
            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

        text = cleanup_text(text)
        new_text = ""
        offensive_words = 0

        with open(_MODULES_DIR / "_bad_words.txt", mode="r", encoding="utf-8") as f:
            bad_words = f.read().splitlines()
            bad_words_plural = [bad_words[i] + "s" for i in range(len(bad_words))]
            bad_words = bad_words + bad_words_plural

        for word in text:
            if word.lower() in bad_words:
                offensive_words += 1
                word = word.replace(word, "*" * len(word))
            new_text += f"{word} "
        new_text = new_text.replace(" .", ".")
        print(
            Panel(
                renderable=new_text,
                padding=(2, 2),
                title="[reverse]Censored Text[/reverse]",
                border_style="bold violet",
                box=box.DOUBLE_EDGE,
            )
        )

        print(
            Panel(
                renderable=f"[bold]Offensive words censored:[/bold][bold red] {offensive_words} 😤[/bold red]",
                title="[reverse]Censored Words[/reverse]",
            )
        )


def censor_bad_words_not_strict(text: str) -> None:
    """
    Removes the bad words from the text and replaces them with asterisks partially and prints the censor text

    1. First we check if the text is a URL, if yes, then we parse the text from it and then use the model
    2. If the text is not a URL, then we directly use the model
    3. Remove the punctuations and convert text to lowercase
    4. Read the bad words from the file and store them in a list
    5. Split the text into words and for each word, we check if it is a bad word, if yes, then we partially replace it with asterisks
    6. Print the censored text and the number of bad words censored

    Args:
        text (str): text that needs to be censored
    """
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="monkey", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Censoring...", total=None)
        # ----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )
            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

        with open(_MODULES_DIR / "_bad_words.txt", mode="r", encoding="utf-8") as f:
            bad_words = f.read().splitlines()
            bad_words_plural = [bad_words[i] + "s" for i in range(len(bad_words))]
            bad_words = bad_words + bad_words_plural

        text = cleanup_text(text)
        new_text = ""
        offensive_words = 0

        for word in text:
            word = str(word)
            if word.lower() in bad_words:
                offensive_words += 1
                if len(word) <= 3:
                    word = word.replace(word, "*" * len(word))
                elif len(word) <= 5:
                    # replace the middle character with asterisk
                    word = word.replace(word[1], "*")
                    word = word.replace(word[2], "*")
                    word = word.replace(word[3], "*")
                else:
                    word = word.replace(word[2:5], "***")
            new_text += f"{word} "
        new_text = new_text.replace(" .", ".")
        print(
            Panel(
                renderable=new_text,
                padding=(2, 2),
                title="[reverse]Censored Text[/reverse]",
                border_style="bold violet",
                box=box.DOUBLE_EDGE,
            )
        )
        print(
            Panel(
                renderable=f"[bold]Offensive words censored:[/bold][bold red] {offensive_words} 😤[/bold red] ",
                padding=(1, 1),
                title="[reverse]Censored Words[/reverse]",
            )
        )


def readability_index(text: str) -> None:
    """
    Prints the readability index of the text and the summary of the index

    1. First we check if the text is a URL, if yes, then we parse the text from it and then use the model
    2. If the text is not a URL, then we directly use the model
    3. Remove the punctuations and convert text to lowercase
    4. Split the text into words and count the number of words
    5. Split the text into sentences and count the number of sentences
    6. The function then calculates the readability index using the textstat module and stores it in the "readability_index" variable.
    7. Print the readability index and the summary of the index

    Args:
        text (str): text to be analyzed
    """
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold green"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing Text...", total=None)
        # ----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )

            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

        text = cleanup_text(text)
        text = " ".join(text)

        readability_index = textstat.flesch_reading_ease(text)

        if readability_index > 90:
            index_desc = "Very Easy"
        elif readability_index > 80:
            index_desc = "Easy"
        elif readability_index > 70:
            index_desc = "Fairly Easy"
        elif readability_index > 60:
            index_desc = "Standard"
        elif readability_index > 50:
            index_desc = "Fairly Difficult"
        elif readability_index > 30:
            index_desc = "Difficult"
        else:
            index_desc = "Very Confusing"

        print(
            Panel(
                title="[b reverse]Readability Index[/b reverse]",
                title_align="center",
                padding=(2, 2),
                border_style="bold magenta1",
                box=box.DOUBLE,
                renderable=f"[b r blue]Lexicon Count[/b r blue]: {textstat.lexicon_count(text, removepunct=True)}\n\n[b r green]Character Count (without spaces)[/b r green]: {textstat.char_count(text)}\n\n[b r yellow2]Sentence Count[/b r yellow2]: {textstat.sentence_count(text)}\n\n[b r gold1]Words Per Sentence[/b r gold1]: {textstat.avg_sentence_length(text)}\n\n[b r white]Readability Index[/b r white]: {textstat.flesch_reading_ease(text)}",
            )
        )


def extract_difficult_words(text: str) -> None:
    """Extracts the difficult words from the text and prints them.

    Uses the ``_most_common_words.txt`` file to determine difficult words, and
    spaCy NER to remove proper nouns.  Requires the ``[nlp]`` optional extras.

    Args:
        text (str): text or URL to be analysed.
    """
    if not _require_nlp():
        return
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold gold1"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold white",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Checking URL...", total=None)
        # ----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )
            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )
            text = cleanup_text(text)
            text = " ".join(text)

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold gold1"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold white",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Removing Common Words...", total=None)
        # ----------------- Spinner -----------------#

        with open(
            file="modules/_most_common_words.txt", mode="r", encoding="utf-8"
        ) as f:
            simple_words = f.read().splitlines()
        text = cleanup_text(text)
        article_word_count = len(text)

        # remove full stop from the words
        text = [word for word in text if "." not in word]
        difficult_words = [word for word in text if word.lower() not in simple_words]

        # filter out duplicate words
        difficult_words = list(set(difficult_words))

        # remove plurals of the same word
        for word in difficult_words:
            if word[-1] == "s" and word[:-1] in difficult_words:
                difficult_words.remove(word)

        # remove plurals of which singular is in the simple words list
        for word in difficult_words:
            if word[-1] == "s" and word[:-1] in simple_words:
                difficult_words.remove(word)

        # remove words that end with 'ing'
        for word in difficult_words:
            if word[-3:] == "ing":
                difficult_words.remove(word)

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold gold1"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold white",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Removing Named Entities...", total=None)
        # ----------------- Spinner -----------------#

        # remove all named entities
        difficult_words = " ".join(difficult_words)

        # Loading the NLP model
        nlp = spacy.load("en_core_web_sm")

        nlp_text = nlp(difficult_words)
        entities = [entity.text for entity in nlp_text.ents]

        difficult_words = [
            word for word in difficult_words.split() if word not in entities
        ]

        # remove all uppercase words
        difficult_words = [word for word in difficult_words if word.islower()]

        # remove mispelled words
        import spellchecker

        spell = spellchecker.SpellChecker()
        difficult_words = [
            word
            for word in difficult_words
            if word not in spell.unknown(difficult_words)
        ]

        difficult_words.sort()
        print(
            Panel(
                title="[b reverse navajo_white1]  Success!  [/b reverse navajo_white1]",
                title_align="center",
                padding=(1, 1),
                border_style="navajo_white1",
                box=box.DOUBLE,
                renderable=f"[bold]Content Length:[/bold] [bold blue]{article_word_count}[/bold blue] words\nExtracted [bold blue]{len(difficult_words)}[/bold blue] difficult words",
            ),
        )

        difficult_words = [
            Panel(
                f"[b gold1 dim]{idx}[/b gold1 dim]. [i thistle1]{word}[/i thistle1]",
                expand=True,
                box=box.SQUARE,
                border_style="pale_violet_red1",
            )
            for idx, word in enumerate(difficult_words, start=1)
        ]
        # ----------------- Columns -----------------#

        print(Columns(difficult_words, expand=True))

        # ----------------- Columns -----------------#


def sentiment_score_to_summary(sentiment_score: int) -> str:
    """
    Converts the sentiment score to a summary of the score

    Args:
        sentiment_score (int): sentiment score

    Returns:
        str: summary of the sentiment score
    """

    if sentiment_score == 1:
        return "Extremely Negative"
    elif sentiment_score == 2:
        return "Somewhat Negative"
    elif sentiment_score == 3:
        return "Generally Neutral"
    elif sentiment_score == 4:
        return "Somewhat Positive"
    elif sentiment_score == 5:
        return "Extremely Positive"


def sentiment_analysis(content: str) -> None:
    """Perform sentiment analysis on the text and print the result.

    Uses ``nlptown/bert-base-multilingual-uncased-sentiment`` via Hugging Face
    Transformers.  Requires the ``[nlp]`` optional extras.

    Args:
        content (str): text or URL to be analysed.
    """
    if not _require_nlp():
        return

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="smiley", style="bold green"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold white",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Getting Sentiment...", total=None)
        # ----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(content):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )
            text = parse_text_from_web(content)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )
            text = cleanup_text(content)
            text = " ".join(text)

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

        tokenizer = AutoTokenizer.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment"
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment"
        )
        tokens = tokenizer.encode(
            text, return_tensors="pt", truncation=True, padding=True
        )
        result = model(tokens)
        result.logits
        sentiment_score = int(torch.argmax(result.logits)) + 1
        outcome = sentiment_score_to_summary(sentiment_score)
        if outcome in ["Extremely Negative", "Somewhat Negative"]:
            emoji = "😞"

        elif outcome == "Generally Neutral":
            emoji = "😐"

        elif outcome in ["Somewhat Positive", "Extremely Positive"]:
            emoji = "😀"

        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]Sentiment Analysis Verdict:[/bold blue] {sentiment_score_to_summary(sentiment_score)} {emoji}",
            )
        )


# TODO @atharva check this
def summarize_text_util(text: str, per: int) -> str:
    """
    Summarizes the text using the OpenAI API (modern client, ``openai>=1.0``).

    Args:
        text (str): text to be summarized
        per (int): percentage of the text to be summarized (currently unused,
            kept for interface compatibility)

    Returns:
        str: summarized text
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following text concisely:\n\n{text}",
                }
            ],
            temperature=0,
        )
        result = response.choices[0].message.content or ""
        # remove escape characters and newlines
        result = re.sub(r"\\n", " ", result)
        if "Summary:" in result:
            result = result.split("Summary:")[1]
        return result.strip()
    except Exception as exc:
        # Graceful degradation: fall back to extractive summarisation with spacy
        if not _NLP_AVAILABLE:
            return text
        nlp = spacy.load("en_core_web_sm")  # type: ignore[name-defined]
        doc = nlp(text)
        tokens = [token.text for token in doc]
        word_frequencies: dict = {}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS) and word.text.lower() not in punctuation:
                word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1
        if not word_frequencies:
            return text
        max_frequency = max(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] /= max_frequency
        sentence_tokens = list(doc.sents)
        sentence_scores: dict = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]
        select_length = max(1, int(len(sentence_tokens) * per))
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
        return "".join(word.text for word in summary)


def summarize_text(content: str, file: Optional[bool] = False) -> None:
    """
    Print the summarized text or internet article.

    1. Check if the content is a URL or text
    2. If URL, then parse the text from it and then use the model
    3. If text, then directly use the model
    4. Clean up the text from any unnecessary characters, full stops, and convert it to lowercase.
    5. It summarizes the text using the summarize_text_util function.
    6. If the input is a URL, it prints the headline of the article as well.
    7. If the output is a file, it saves the summary to a file called summary.txt.

    Args:
        text (str): Text that is to be summarized
    """

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold blue"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold white",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Summarizing...", total=None)
        # ----------------- Spinner -----------------#

        if isWebURL := check_url_or_text(content):
            print(
                Panel(
                    title="[b reverse green]  Processing...  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="URL detected 🌐",
                )
            )

            # this is just get the headings
            r = requests.get(content)
            soup = BeautifulSoup(r.content, "html.parser")
            headline = soup.find("h1").get_text()

            # this gets the body of the article.
            text = parse_text_from_web(content)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(
                Panel(
                    title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Processing text... 📃",
                )
            )
            text = cleanup_text(content)
            text = " ".join(text)

        # HANDLE INVALID URLS
        if text == -1:
            print(URL_INVALID_PANEL)
            return

        text_summary = summarize_text_util(text, 0.2)

        if not file:
            if isWebURL:
                print(
                    Panel(
                        title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable=f"[bold blue]Length of the article:[/bold blue] [bold]{len(text)}[/bold] characters\n\n[bold blue]Length of the summary:[/bold blue] [bold]{len(text_summary)} [/bold]characters \n\n[bold blue]Headline:[/bold blue] [bold]{headline}[/bold]\n\n[b green u]Summary:[/b green u]\n{text_summary}",
                    )
                )
            else:
                print(
                    Panel(
                        title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable=f"[bold blue]Length of the article:[/bold blue] [bold]{len(text)}[/bold] characters  \n\n [bold blue]Length of the summary:[/bold blue][bold]{len(text_summary)}[/bold] characters\n\n[bold blue]Summary:[/bold blue]\n{text_summary}",
                    )
                )

        if file:
            # writing to a .txt file
            with open("summary.txt", "w", encoding="utf-8") as f:
                f.write(f"Length of the article: {len(text)} characters\n\n")
                f.write(f"Length of the summary:{len(text_summary)} characters\n\n")
                if isWebURL:
                    f.write(str(f"Headline:\n{headline}\n\n"))
                f.write(
                    "------------------------------------------------------------\n\n"
                )
                f.write(f"Summary:\n{text_summary}\n\n")

            print(
                Panel(
                    title="[b reverse green]  Summary Exported!  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="[bold green]Summary saved[/bold green] to [bold]summary.txt[/bold]",
                )
            )
        # TODO: writing to a .md file
