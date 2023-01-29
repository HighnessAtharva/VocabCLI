from typing import *

import nltk
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from spellchecker import SpellChecker


def spell_checker(string: str) -> str:
    """
    This function takes a string as input and returns a string with misspelled words highlighted in red.
    
    1. Split the string based on punctuation.
    2. Find those words that may be misspelled.
    3. Highlight the misspelled words in red.
    4. Return the string with misspelled words highlighted in red.
    """

    spell = SpellChecker()

    # string = "I havv goood speling! The age of the Universe is 13.8 billion years. I am 13 years old. knownsd is a surname."

    # split based on punctuation
    tokenized = string.split()
    tokenized = nltk.regexp_tokenize(string, r"\w+|\$[\d\.]+|\S+")

    # find those words that may be misspelled
    misspelled = spell.unknown(tokenized)
    sentence = "".join(
        f"[red s]{word}[/red s] "
        if word in misspelled and word.isalpha()
        else f"{word} "
        for word in tokenized
    )
    sentence = sentence.replace(" .", ".")
    print(
        Panel(
            title="[b reverse red]Mispelled words[/b reverse red]",
            title_align="center",
            border_style="red",
            renderable=sentence,
        )
    )
