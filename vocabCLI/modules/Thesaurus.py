import nltk
from Dictionary import *
from nltk.corpus import wordnet
from rich import print, box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

# nltk.download('wordnet')
# nltk.download('omw-1.4')

# todo @anay - formatting can be improved, add color, styles and emojis. Need to change column style.
# sourcery skip: for-append-to-extend, remove-redundant-if
def find_synonym(query: str) -> None:
    """
    Finds the synonyms of the query word
    
    1. Connects to the API
    2. Checks if the API returned a response
    3. If it did, it loops through the response and adds the synonyms to a list
    4. If the list is empty, it uses the NLTK library to find synonyms
    5. If it still can't find any synonyms, it prints an error message
    6. If it did find synonyms, it prints them in columns

    Args:
        query (str): Word to find synonyms for.
    """
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="point", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Searching Synonyms", total=None)
        # ----------------- Spinner -----------------#

        synonyms = []
        if not (response := connect_to_api(query)):
            return

        # check from api and add to list
        for meaningNumber in response["meanings"]:
            for synonym in meaningNumber["synonyms"]:
                if query not in synonym and " " not in synonym:
                    synonyms.append(synonym)

        # remove special characters and numbers
        for x in synonyms:
            if x.isalpha() == False:
                synonyms.remove(x)

        # if none returned from API, fallback to NLTK and append the list
        if not len(synonyms):
            for syn in wordnet.synsets(query):
                synonyms.extend(lm.name() for lm in syn.lemmas())
                if synonyms := list(filter(lambda x: "_" not in x, synonyms)):
                    synonyms = list(filter(lambda x: x != query, synonyms))

        # finally print the list
        if len(synonyms):
            print(
                Panel(
                    f" [reverse bold green]Synonyms[/reverse bold green] of [bold blue underline]{query}[/bold blue underline] are 👇"
                )
            )
            synonyms = [
                Panel(f"[b gold1 dim]{idx}[/b gold1 dim]. [sea_green1]{synonym}[sea_green1]", 
                      expand=True,
                      box=box.SQUARE)
                for idx, synonym in enumerate(synonyms, start=1)
            ]

            # ----------------- Columns -----------------#

            print(Columns(synonyms, expand=True))

            # ----------------- Columns -----------------#

        else:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    box=box.SQUARE,
                    renderable=f"No synonyms found for {query}",
                )
            )


# todo @anay - formatting can be improved, add color, styles and emojis. Need to change column style.
def find_antonym(query: str) -> None:  # sourcery skip: for-append-to-extend
    """
    Finds the antonyms of the query word
    
    1. Connects to the API
    2. Checks if the API returned a response
    3. If it did, it loops through the response and adds the antonyms to a list
    4. If the list is empty, it uses the NLTK library to find antonyms
    5. If it still can't find any antonyms, it prints an error message
    6. If it did find antonyms, it prints them in columns

    Args:
        query (str): Word to find antonyms for.
    """

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="point", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Searching Antonyms", total=None)
        # ----------------- Spinner -----------------#

        antonyms = []
        if not (response := connect_to_api(query)):
            return

        for meaningNumber in response["meanings"]:
            for antonym in meaningNumber["antonyms"]:
                if query not in antonym and " " not in antonym:
                    antonyms.append(antonym)

        antonyms = list(set(antonyms))
        # if none returned from API, fallback to NLTK and append the list
        if not len(antonyms):
            for syn in wordnet.synsets(query):
                antonyms.extend(lm.name() for lm in syn.lemmas() if lm.antonyms())
                if antonyms := list(filter(lambda x: "_" not in x, antonyms)):
                    antonyms = list(filter(lambda x: x != query, antonyms))

        # remove special characters and numbers
        for x in antonyms:
            if x.isalpha() == False:
                antonyms.remove(x)

        # finally print the list
        if len(antonyms):
            print(
                Panel(
                    f" [reverse bold red]Antonyms[/reverse bold red] of [bold blue underline]{query}[/bold blue underline] are 👇"
                )
            )
            antonyms = [
                Panel(f"[b gold1 dim]{idx}[/b gold1 dim]. [red]{antonym}[red]", 
                      expand=True, 
                      box=box.SQUARE) for idx, antonym in enumerate(antonyms, start=1)
            ]

            # ----------------- Columns -----------------#

            print(Columns(antonyms, expand=True))

            # ----------------- Columns -----------------#

        else:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"No antonyms found for {query}",
                )
            )
