from spellchecker import SpellChecker
from rich import print
from typing import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import nltk

spell = SpellChecker()

string = "I havv goood speling! The age of the Universe is 13.8 billion years. I am 13 years old. knownsd is a surname."


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
sentence=sentence.replace(" .",".")
print(Panel(title="[b reverse red]Mispelled words[/b reverse red]",title_align="center",  border_style="red", renderable=sentence))