from nltk.corpus import wordnet
import nltk
from rich import print
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

# nltk.download('wordnet')
# nltk.download('omw-1.4')

def find_synonym(query:str):
    synonyms = []
    for syn in wordnet.synsets(query):
        synonyms.extend(lm.name() for lm in syn.lemmas())
    if synonyms := set(filter(lambda x: "_" not in x, synonyms)):
        synonyms = set(filter(lambda x: x != query, synonyms))
        print(Panel(f" [reverse bold green]Synonyms[/reverse bold green] of [bold blue underline]{query}[/bold blue underline] are ⏭"))
        synonyms = [Panel(f"[sea_green1]{synonym}[sea_green1]", expand=True) for synonym in synonyms]
        print(Columns(synonyms))
    else:
        print(Panel(f"No synonyms found for {query}"))
    print("\n\n")
    
def find_antonym(query:str):
    antonyms = []
    for syn in wordnet.synsets(query):
        antonyms.extend(lm.antonyms()[0].name() for lm in syn.lemmas() if lm.antonyms())
    if antonyms := set(filter(lambda x: "_" not in x, antonyms)):
        print(Panel(f" [reverse bold red]Antonyms[/reverse bold red] of [bold blue underline]{query}[/bold blue underline] are ⏭"))
        antonyms = [Panel(f"[deep_pink4]{antonym}[deep_pink4]", expand=True) for antonym in antonyms]
        print(Columns(antonyms))
    else:
        print(Panel(f"No antonyms found for {query}"))
    print("\n\n")
