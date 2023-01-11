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
sentence=""

# print the original sentence with the misspelled words highlighted (red)
for word in tokenized:
    # check if the word is misspelled and not a punctuation, number or symbol
    if word in misspelled and word.isalpha():
        sentence += f"[red s]{word}[/red s] "
    else:
        sentence += {word}

print(Panel(title="[b reverse red]Mispelled words[/b reverse red]",title_align="center",  border_style="red", renderable=sentence))