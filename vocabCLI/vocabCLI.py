import os
import sys
from typing import *

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel

# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=False,
    rich_markup_mode="rich",
    help="📕[bold green] This is a dictionary and a vocabulary builder CLI.[/bold green] VocabularyCLI is a lightweight Command Line Interface that allows users to look up word definitions, examples, synonyms and antonyms directly via the command line. Powered with several utility based commands our CLI offers rapid and robust Knowledge Base capabilities like Flashcards, Tagging, Word Management, Graph Reporting, Bulk import and export of word lists and is a definitive software for linguaphiles. This application boasts a simple and intuitive interface that is easy to use and is a must have for anyone who wants to expand their vocabulary and improve their language skills. The app also offers advanced Text Classification and Processing via the use of Natural Language Processing. The CLI will be offered with eye-catching Panels, Tables, Animated Symbols, Emojis, Interactive Menus, Spinners, Colored fonts and other rich features that will make the user experience more enjoyable and interactive.",
)


@app.command(
    rich_help_panel="Miscellaneous", help="🔄 Update the JSON response in the cache"
)
def refresh():
    """
    Refreshes the cached content from the API.
    """
    from modules.Database import refresh_cache

    refresh_cache()


@app.command(
    rich_help_panel="Miscellaneous", help="👋🏼 [bold red]Exits[/bold red] the CLI"
)
def bye():
    print(Panel("👋🏼 [bold green]Bye bye![/bold green]"))
    sys.exit(0)


@app.command(
    rich_help_panel="Miscellaneous", help="💻 [bold blue]About[/bold blue] the software"
)
def about():
    """
    Print information about the software.
    """
    from modules.About import print_about_app
    from modules.Banner import print_banner

    console = Console(record=False, color_system="truecolor")
    print_banner(console)
    print_about_app()


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary",
)
def define(
    words: List[str] = typer.Argument(
        ..., help="📚 [bold blue]Word[/bold blue] which is to be defined."
    ),
    short: bool = typer.Option(
        False,
        "--short",
        "-s",
        help="📚 [bold blue]Short definition[/bold blue] of the word.",
    ),
    pronounce: bool = typer.Option(
        False, "--pronounce", "-p", help="📚 [bold blue]Pronounce[/bold blue] the word."
    ),
):
    # sourcery skip: use-named-expression
    """
    Looks up a word in the dictionary.

    Args:
        words (List[str]): Word which is to be defined.
        short (bool, optional): If True, prints the short definition of the word. Defaults to False.
        pronounce (bool, optional): If True, plays the pronunciation of the word. Defaults to False.
    """
    from modules.Dictionary import definition, say_aloud

    for word in words:

        if short:
            definition(word, short=True)

        if not short:
            definition(word, short=False)

        if pronounce:
            say_aloud(query=word)


@app.command(
    "list",
    rich_help_panel="Word Management",
    help="📝 [bold blue]Lists [/bold blue] of all your looked up words",
)
def ListCMD(
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="📝 Lists only words set as [r bold gold1]favorite[/r bold gold1].",
    ),
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="📝 Lists only words set as [r bold green]learning[/r bold green].",
    ),
    mastered: bool = typer.Option(
        None,
        "--mastered",
        "-m",
        help="📝 Lists only words set as [r bold blue]mastered[/r bold blue].",
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="📝 Lists only words with a particular [bold purple4 r]tag[/bold purple4 r].",
    ),
    days: int = typer.Option(
        None,
        "--days",
        "-d",
        help="📝 Lists only words looked up in the [bold aquamarine3]last N days.[/bold aquamarine3]",
    ),
    date: bool = typer.Option(
        False,
        "--date",
        "-D",
        help="📝 Lists only words looked up on a [bold aquamarine3]particular date.[/bold aquamarine3]",
    ),
    last: int = typer.Option(
        None,
        "--last",
        "-L",
        help="📝 Lists only the [bold orange3]last N[/bold orange3] words looked up.",
    ),
    most: int = typer.Option(
        None,
        "--most",
        "-M",
        help="📝 Lists only the [bold orange3]most[/bold orange3] looked up words.",
    ),
    tags: bool = typer.Option(
        False,
        "--tagnames",
        "-T",
        help="📝 Lists only the [bold purple4 r]tags[/bold purple4 r] used by the user.",
    ),
    collection: str = typer.Option(
        None,
        "--collection",
        "-c",
        help="📝 Lists only the words in a particular [bold cyan r]collection[/bold cyan r]",
    ),
    collections: bool = typer.Option(
        False,
        "--collections",
        "-C",
        help="📝 Lists only the [bold cyan1]collections[/bold cyan1] available.",
    ),
):

    """
    Lists all the words looked up by the user.

    Args:
        favorite (bool, optional): If True, prints the list of favorite words. Defaults to False.
        learning (bool, optional): If True, prints the list of words in learning list. Defaults to False.
        mastered (bool, optional): If True, prints the list of words in mastered list. Defaults to False.
        tag (str, optional): If True, prints the list of words with a particular tag. Defaults to None.
        days (str, optional): If True, prints the list of words from last n number of days. Defaults to None.
        date (str, optional):  If True, prints the list of words from a particular date. Defaults to None.
        last (str, optional): If True, prints the list of last searched words. Defaults to None.
        most (str, optional): If True, prints the list of most searched words. Defaults to None.
        tagnames (bool, optional): If True, prints the list of all the tags. Defaults to False.
        collection (Optional[str], optional): If True, prints the list of words from a collection. Defaults to None.
        collections (Optional[bool], optional): If True, prints the list of all the collections. Defaults to False.
    """
    from modules.Utils import show_list
    from modules.WordCollections import show_all_collections, show_words_from_collection

    if favorite:
        show_list(favorite=True)
    if learning:
        show_list(learning=True)
    if mastered:
        show_list(mastered=True)
    if tag:
        show_list(tag=tag)
    if days:
        show_list(days=days)
    if date:
        show_list(date=date)
    if last:
        show_list(last=last)
    if most:
        show_list(most=most)
    if tags:
        show_list(tagnames=True)
    if collection:
        show_words_from_collection(collectionName=collection)
    if collections:
        show_all_collections()

    elif not any(
        [
            favorite,
            learning,
            mastered,
            tag,
            days,
            date,
            last,
            most,
            collection,
            collections,
            tags,
        ]
    ):
        show_list()


@app.command(
    rich_help_panel="Word Management",
    help="💙 [bold green]Sets[/bold green] a word as [bold gold1]favorite[/bold gold1]",
)
def favorite(
    words: List[str] = typer.Argument(
        ..., help="💙 Word to add to [bold gold1]favorites[/bold gold1]."
    ),
):
    """
    Adds a word to the favorite list.

    Args:
        words (List[str]): Word which is to be added to the favorite list.
    """
    from modules.Utils import set_favorite

    for word in words:
        set_favorite(word)


@app.command(
    rich_help_panel="Word Management",
    help="💔 [bold red]Removes[/bold red] the word from [bold gold1]favorites[/bold gold1]",
)
def unfavorite(
    words: List[str] = typer.Argument(
        ...,
        help="💔 [bold blue]Word[/bold blue] to remove from [bold gold1]favorites[/bold gold1]",
    ),
):
    """
    Removes a word from the favorite list.

    Args:
        words (List[str]): Word which is to be removed from the favorite list.
    """
    from modules.Utils import set_unfavorite

    for word in words:
        set_unfavorite(word)


@app.command(
    rich_help_panel="Word Management",
    help="🎓 [bold green]Sets[/bold green] a word as [bold blue]learning[/bold blue]",
)
def learn(
    words: List[str] = typer.Argument(
        ..., help="✍🏼 Word to add to [bold green]learning[/bold green]."
    ),
):
    """
    Adds a word to the learning list.

    Args:
        words (List[str]): Word which is to be added to the learning list.
    """
    from modules.Utils import set_learning

    for word in words:
        set_learning(word)


@app.command(
    rich_help_panel="Word Management",
    help="😪 [bold red]Removes[/bold red] the word from [bold blue]learning[/bold blue]",
)
def unlearn(
    words: List[str] = typer.Argument(
        ..., help="😪 Word to remove from [bold green]learning[/bold green]."
    ),
):
    """
    Removes a word from the learning list.

    Args:
        words (List[str]): Word which is to be removed from the learning list.
    """
    from modules.Utils import set_unlearning

    for word in words:
        set_unlearning(word)


@app.command(
    rich_help_panel="Word Management",
    help="🧠 [bold green]Sets[/bold green] a word as [bold green]mastered[/bold green]",
)
def master(
    words: List[str] = typer.Argument(
        ..., help="🧠 Word to add to [bold blue]mastered[/bold blue]."
    ),
):
    """
    Adds a word to the mastered list.

    Args:
        words (List[str]): Word which is to be added to the mastered list.
    """
    from modules.Utils import set_mastered

    for word in words:
        set_mastered(word)


@app.command(
    rich_help_panel="Word Management",
    help="🤔 [bold red]Removes[/bold red] the word from [bold green]mastered[/bold green]",
)
def unmaster(
    words: List[str] = typer.Argument(
        ..., help="🤔Word to remove from [bold blue]mastered[/bold blue]"
    ),
):
    """
    Removes a word from the mastered list.

    Args:
        words (List[str]): Word which is to be removed from the mastered list.
    """
    from modules.Utils import set_unmastered

    for word in words:
        set_unmastered(word)


@app.command(
    rich_help_panel="Import & Export",
    help="📂 [bold chartreuse1]Exports[/bold chartreuse1] a list of all your looked up words",
)
def export(
    pdf: bool = typer.Option(
        False,
        "--pdf",
        "-P",
        help="📂 [bold green]Export[/bold green] a list of your looked up words in [bold purple3 r] PDF format[/bold purple3 r].",
    ),
):
    """
    Exports a list of all your looked up words.

    Args:
        pdf (bool, optional): If True, exports a list of your looked up words in PDF format. Defaults to False.
    """
    from modules.ImportExport import export_to_csv, export_to_pdf

    if pdf:
        export_to_pdf()
    else:
        export_to_csv()


@app.command(
    "import",
    rich_help_panel="Import & Export",
    help="🔼 [bold blue]Imports[/bold blue] a list words in the application",
)
def Import():
    """
    Imports a list of words in the application.
    """

    from modules.ImportExport import import_from_csv

    import_from_csv()


@app.command(
    rich_help_panel="Word Management", help="🔖 [bold blue]Tags[/bold blue] a word"
)
def tag(
    words: List[str] = typer.Argument(..., help="🔖 Words to be tagged"),
    tag: str = typer.Option(
        ...,
        "--name",
        "-n",
        help="🔖 [bold purple4 r]Tag[/bold purple4 r] to add to the words",
    ),
):

    """
    Tags a word.

    Args:
        words (List[str]): Words to tagged.
        tag (str): Tag to add to the words.
    """

    from modules.Utils import add_tag

    for word in words:
        add_tag(word, tag)


@app.command(
    rich_help_panel="Word Management",
    help="🔪[bold red] Removes[/bold red] tag of a word in the dictionary",
)
def untag(
    words: List[str] = typer.Argument(
        ..., help="✂ Word to remove [bold purple4 r]tag[/bold purple4 r] from"
    ),
):
    """
    Remove tag of a word in the dictionary.

    Args:
        words (List[str]): Word to remove tag from.
    """
    from modules.Utils import remove_tag

    for word in words:
        remove_tag(word)


@app.command(
    rich_help_panel="Vocabulary Builder", help="📈 Periodic comparison of words learned"
)
def rate(
    today: bool = typer.Option(
        False,
        "--today",
        "-t",
        help="📊 Get [bold orchid1]learning rate[/bold orchid1] [u]today[/u]",
    ),
    week: bool = typer.Option(
        False,
        "--week",
        "-w",
        help="📊 Get [bold orchid1]learning rate[/bold orchid1] this [u]week[/u]",
    ),
    month: bool = typer.Option(
        False,
        "--month",
        "-m",
        help="📊 Get [bold orchid1]learning rate[/bold orchid1] this [u]month[/u]",
    ),
    year: bool = typer.Option(
        False,
        "--year",
        "-y",
        help="📊 Get [bold orchid1]learning rate[/bold orchid1] this [u]year[/u]",
    ),
):

    """
    Gives the number of words you have learned in a particular time period with a comparison of a previous time period.

    Args:
        today (bool, optional): If True, get learning rate today. Defaults to False.
        week (bool, optional): If True, get learning rate this week. Defaults to False.
        month (bool, optional): If True, get learning rate this month. Defaults to False.
        year (bool, optional): If True, get learning rate this year. Defaults to False.
    """

    from modules.Utils import get_lookup_rate

    if today:
        get_lookup_rate(today=True)
    elif week:
        get_lookup_rate(week=True)
    elif month:
        get_lookup_rate(month=True)
    elif year:
        get_lookup_rate(year=True)
    elif not any([today, week, month, year]):
        # default is today
        get_lookup_rate(today=True)


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="🔎 Find [bold green]synonyms[/bold green] for a word",
)
def synonym(
    words: List[str] = typer.Argument(
        ..., help="🔎 Word to search [bold green]synonyms[/bold green] for"
    ),
):
    """
    Find synonyms for a word.

    Args:
        words (List[str]): Word to search synonyms for.
    """
    from modules.Thesaurus import find_synonym

    for word in words:
        find_synonym(word)


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="❌ Find [bold red]antonyms[/bold red] for a word",
)
def antonym(
    words: List[str] = typer.Argument(
        ..., help="❌ Word to search [bold red]antonyms[/bold red] for"
    ),
):
    """
    Find antonyms for a word.

    Args:
        words (List[str]): Word to search antonyms for.
    """
    from modules.Thesaurus import find_antonym

    for word in words:
        find_antonym(word)


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="🔁 Get a [bold bright_magenta]lookup history[/bold bright_magenta] of a word",
)
def history(
    words: List[str] = typer.Argument(
        ...,
        help="🔁 Word to get [bold bright_magenta]lookup history[/bold bright_magenta] for",
    ),
):
    """
    Get a lookup history of a word.

    Args:
        words (List[str]): Word to get lookup history for.
    """
    from modules.Utils import fetch_word_history

    for word in words:
        fetch_word_history(word)


@app.command(
    rich_help_panel="Word Management",
    help="🚮 [bold red]Deletes[/bold red] the word from the database",
)
def delete(
    words: List[str] = typer.Argument(
        None, help="🚮 Word to be [bold red]deleted[/bold red]"
    ),
    mastered: bool = typer.Option(
        False,
        "--mastered",
        "-m",
        help="🚮 [bold red]Delete[/bold red] all [bold blue r]mastered[/bold blue r] words.",
    ),
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="🚮 [bold red]Delete[/bold red] all [bold green r]learning[/bold green r] words.",
    ),
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="🚮 [bold red]Delete[/bold red] all [bold gold1 r]favorite[/bold gold1 r] words.",
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="🚮 [bold red]Delete[/bold red] all words with a particular [bold purple4 r]tag[/bold purple4 r].",
    ),
):

    """
    Deletes the word from the database.

    Args:
        mastered (bool, optional): Deletes all mastered words. Defaults to False.
        learning (bool, optional): Deletes all learning words. Defaults to False.
        favorite (bool, optional): Deletes all favorite words. Defaults to False.
        tag (str, optional): Tag of words to be deleted. Defaults to None.
        words (List[str], optional): Word to be deleted. Defaults to None.
    """
    from modules.Utils import (
        delete_all,
        delete_favorite,
        delete_learning,
        delete_mastered,
        delete_word,
        delete_words_from_tag,
    )

    if mastered:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your mastered list[/b]?",
            )
        )

        if sure := typer.confirm(""):
            delete_mastered()
        else:
            print(Panel("OK, not deleting anything."))

    elif learning:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your learning list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            delete_learning()
        else:
            print(Panel("OK, not deleting anything."))

    elif favorite:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your favorite list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            delete_favorite()
        else:
            print(Panel("OK, not deleting anything."))

    elif tag:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from tag {tag}[/b]?",
            )
        )
        if sure := typer.confirm(""):
            delete_words_from_tag(tag)
        else:
            print(Panel("OK, not deleting anything."))

    elif words:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to delete these [b]{len(words)} words from your list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            for word in words:
                delete_word(word)
        else:
            print(Panel("OK, not deleting anything."))

    elif not any([mastered, learning, favorite, tag, words]):
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            delete_all()
        else:
            print(Panel("OK, not deleting anything."))


@app.command(
    rich_help_panel="Word Management", help="🧹 [bold red]Clears[/bold red] all lists."
)
def clear(
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="🧹 [bold red]Clear[/bold red] all words in your [bold green r]learning[/bold green r] list.",
    ),
    master: bool = typer.Option(
        False,
        "--mastered",
        "-m",
        help="🧹 [bold red]Clear[/bold red] all words in your [bold blue r]mastered[/bold blue r] list.",
    ),
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="🧹 [bold red]Clear[/bold red] all words in your [bold gold1 r]favorite[/bold gold1 r] list.",
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="🧹 [bold red]Clear[/bold red] all words with a particular [bold purple4 r]tag[/bold purple4 r].",
    ),
):

    """
    Clears all the words from the lists.

    Args:
        learning (bool, optional): If True, clears all the words from the learning list. Defaults to False.
        master (bool, optional): If True, clears all the words from the mastered list. Defaults to False.
        favorite (bool, optional): If True, clears all the words from the favorite list. Defaults to False.
        tag (str, optional): If True, clears all the words with a particular tag. Defaults to None.
    """

    from modules.Utils import (
        clear_all_words_from_tag,
        clear_favorite,
        clear_learning,
        clear_mastered,
    )

    if learning:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your learning list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            clear_learning()
        else:
            print(Panel("OK, not clearing anything."))

    elif master:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your mastered list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            clear_mastered()
        else:
            print(Panel("OK, not clearing anything."))

    elif favorite:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your favorite list[/b]?",
            )
        )
        if sure := typer.confirm(""):
            clear_favorite()
        else:
            print(Panel("OK, not clearing anything."))

    elif tag:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your tag {tag}[/b]?",
            )
        )
        if sure := typer.confirm(""):
            clear_all_words_from_tag(tag)
        else:
            print(Panel(f"OK, not learning any words from the tag {tag}."))

    else:
        raise typer.BadParameter(
            message="Please specify a list to clear. Use --help for more info."
        )


@app.command(rich_help_panel="Vocabulary Builder", help="🔀 Gets a random word")
def random(
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="🔀 Get a [u]random[/u] [bold green r]learning[/bold green r] word.",
    ),
    mastered: bool = typer.Option(
        False,
        "--mastered",
        "-m",
        help="🔀 Get a [u]random[/u] [bold blue r]mastered[/bold blue r] word.",
    ),
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="🔀 Get a [u]random[/u] [bold gold1 r]favorite[/bold gold1 r] word.",
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="🔀 Get a [u]random[/u] word from a particular [bold purple4 r]tag[/bold purple4 r]",
    ),
    collection: str = typer.Option(
        None,
        "--collection",
        "-c",
        help="🔀 Get a [u]random[/u] word from a particular [bold cyan r]collection[/bold cyan r]",
    ),
):

    """
    Gets a random word.

    Args:
        learning (bool, optional): Get a random learning word. Defaults to False.
        mastered (bool, optional): Get a random mastered word. Defaults to False.
        favorite (Optional[bool], optional): Get a random favorite word. Defaults to False.
        tag (Optional[str], optional): Get a random word from a particular tag. Defaults to None.
        collection (Optional[str], optional): Get a random word from a particular collection. Defaults to None.
    """

    from modules.Utils import (
        get_random_word_definition_from_api,
        get_random_word_from_favorite_set,
        get_random_word_from_learning_set,
        get_random_word_from_mastered_set,
        get_random_word_from_tag,
    )
    from modules.WordCollections import get_random_word_from_collection

    if learning:
        get_random_word_from_learning_set()
    elif mastered:
        get_random_word_from_mastered_set()
    elif favorite:
        get_random_word_from_favorite_set()
    elif tag:
        get_random_word_from_tag(tag)
    elif collection:
        get_random_word_from_collection(collection)
    elif not any([learning, mastered, tag, collection, favorite]):
        get_random_word_definition_from_api()


@app.command(
    rich_help_panel="Vocabulary Builder", help="💡 Revise words from your learning list"
)
def revise(
    number: int = typer.Option(
        None,
        "--number",
        "-n",
        help="💡 Number of words to [u]revise[/u] in random order.",
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="💡 [u]Revise[/u] words in a particular [bold purple4 r]tag[/bold purple4 r].",
    ),
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="💡 [u]Revise[/u] words in your [bold green r]learning[/bold green r] list.",
    ),
    mastered: bool = typer.Option(
        False,
        "--mastered",
        "-m",
        help="💡 [u]Revise[/u] words in your [bold blue r]mastered[/bold blue r] list.",
    ),
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="💡 [u]Revise[/u] words in your [bold gold1 r]favorite[/bold gold1 r] list.",
    ),
    collection: str = typer.Option(
        None,
        "--collection",
        "-c",
        help="💡 [u]Revise[/u] words in a particular [bold cyan r]collection[/bold cyan r].",
    ),
):
    # sourcery skip: remove-redundant-if
    """
    Revise words from your learning list.

    Args:
        number (int, optional): Number of words to revise. Defaults to None.
        tag (str, optional): Tag of words to revise. Defaults to None.
        learning (Optional[bool], optional): Revise words in your learning list. Defaults to False.
        mastered (Optional[bool], optional): Revise words in your mastered list. Defaults to False.
        favorite (Optional[bool], optional): Revise words in your favorite list. Defaults to False.
        collection (Optional[str], optional): Revise words in a particular collection. Defaults to None.
    """

    from modules.Study import (
        revise_all,
        revise_collection,
        revise_favorite,
        revise_learning,
        revise_mastered,
        revise_tag,
    )

    if not any([learning, mastered, favorite, collection, tag]) and not number:
        revise_all()

    elif number and not any([learning, mastered, favorite, collection, tag]):
        revise_all(number=number)

    elif tag and not number:
        revise_tag(tag=tag)
    elif tag and number:
        revise_tag(number=number, tag=tag)

    elif learning and not number:
        revise_learning()
    elif learning and number:
        revise_learning(number=number)

    elif mastered and not number:
        revise_mastered()
    elif mastered and number:
        revise_mastered(number=number)

    elif favorite and not number:
        revise_favorite()
    elif favorite and number:
        revise_favorite(number=number)

    elif collection and not number:
        revise_collection(collectionName=collection)
    elif collection and number:
        revise_collection(number=number, collectionName=collection)

    else:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="Cannot combine these arguments",
            )
        )


# TODO: - need to find a way to force break out of the quiz using Ctrl+C, currently it only aborts the current word
@app.command(
    rich_help_panel="Vocabulary Builder", help="❓ Take a quiz on word definitions"
)
def quiz(
    number: int = typer.Option(
        None,
        "--number",
        "-n",
        help="❓ Limit the number of words to [i u]quiz[/i u] on.",
        min=4,
    ),
    tag: str = typer.Option(
        None,
        "--tag",
        "-t",
        help="❓ Take a [i u]quiz[/i u] on words in a particular [bold purple4 r]tag[/bold purple4 r]",
    ),
    learning: bool = typer.Option(
        False,
        "--learning",
        "-l",
        help="❓ Take a [i u]quiz[/i u] on words in your [bold green r]learning[/bold green r] list",
    ),
    mastered: bool = typer.Option(
        False,
        "--mastered",
        "-m",
        help="❓ Take a [i u]quiz[/i u] on words in your [bold blue r]mastered[/bold blue r] list",
    ),
    favorite: bool = typer.Option(
        False,
        "--favorite",
        "-f",
        help="❓ Take a [i u]quiz[/i u] on words in your [bold gold1 r]favorite[/bold gold1 r] list",
    ),
    collection: str = typer.Option(
        None,
        "--collection",
        "-c",
        help="❓ Take a [i u]quiz[/i u] on words in a particular [bold cyan r]collection[/bold cyan r]",
    ),
    history: bool = typer.Option(
        False,
        "--history",
        "-h",
        help="❓ Show [i u]quiz[/i u] [bold orchid2]history[/bold orchid2] and [bold pink1]statistics[/bold pink1]",
    ),
):
    # sourcery skip: remove-redundant-if
    """
    Take a quiz on words in your learning list.

    Args:
        number (int, optional): Number of words to quiz on. Defaults to 10.
        tag (str, optional): Tag of words to quiz on. Defaults to None.
        learning (Optional[bool], optional): Take a quiz on words in your learning list. Defaults to False.
        mastered (Optional[bool], optional): Take a quiz on words in your mastered list. Defaults to False.
        favorite (Optional[bool], optional): Take a quiz on words in your favorite list. Defaults to False.
        collection (Optional[str], optional): Take a quiz on words in a particular collection. Defaults to None.
    """
    from modules.Study import (
        quiz_all,
        quiz_collection,
        quiz_favorite,
        quiz_learning,
        quiz_mastered,
        quiz_tag,
        show_quiz_history,
    )

    if not any([learning, mastered, favorite, collection, tag, history]) and not number:
        quiz_all()

    elif number and not any([learning, mastered, favorite, collection, tag, history]):
        quiz_all(number=number)

    elif tag and not number:
        quiz_tag(tag=tag)
    elif tag and number:
        quiz_tag(number=number, tag=tag)

    elif learning and not number:
        quiz_learning()
    elif learning and number:
        quiz_learning(number=number)

    elif mastered and not number:
        quiz_mastered()
    elif mastered and number:
        quiz_mastered(number=number)

    elif favorite and not number:
        quiz_favorite()
    elif favorite and number:
        quiz_favorite(number=number)

    elif collection and not number:
        quiz_collection(collectionName=collection)
    elif collection and number:
        quiz_collection(number=number, collectionName=collection)

    elif history:
        show_quiz_history()

    else:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="Cannot combine these arguments",
            )
        )


@app.command(
    rich_help_panel="Stats", help="📊 Generate Graphical Charts based on your vocabulary"
)
def graph(
    topWordsBar: int = typer.Option(
        None,
        "--topwordsbar",
        "-twb",
        help="📊 [i u]Bar Graph[/i u] of Top N Most Looked Up Words",
        max=25,
        min=1,
    ),
    topTagsBar: int = typer.Option(
        None,
        "--toptagsbar",
        "-ttb",
        help="📊 [i u]Bar Graph[/i u] of Top N Tags with the most words.",
        max=10,
        min=1,
    ),
    topWordsPie: bool = typer.Option(
        False,
        "--topwordspie",
        "-twp",
        help="📊 [i u]Pie Chart[/i u] of Top 10 Most Looked Up Words",
    ),
    topTagsPie: bool = typer.Option(
        False,
        "--toptagspie",
        "-ttp",
        help="📊 [i u]Pie Chart[/i u] of Top 10 Tags with the most words.",
    ),
    lookupWeek: bool = typer.Option(
        False,
        "--lookupweek",
        "-lw",
        help="📊 [i u]Bar Graph[/i u] of the word count distribution for days in the past [b u]week[/b u].",
    ),
    lookupMonth: bool = typer.Option(
        False,
        "--lookupmonth",
        "-lm",
        help="📊 [i u]Bar Graph[/i u] of the word count distribution for days in the past [b u]month[/b u].",
    ),
    learnVSmaster: bool = typer.Option(
        False,
        "--learnvsmaster",
        "-lvm",
        help="📊 Stacked Graph the number of words in your learning list vs. your mastered list.",
    ),
    wordCountByCollection: bool = typer.Option(
        False,
        "--wordcategories",
        "-wc",
        help="📊 Bar Graph of the number of words in a category domain.",
    ),
    # slider: bool = typer.Option(False, "--slider", "-s", help="Shows all graphs one by one in a slider.")
):
    """
    Generate Graphical Charts based on your vocabulary.

    Args:
        topWordsBar (Optional[int], optional): Visualizes the top N most looked up words. Defaults to None.
        topTagsBar (int, optional): Visualizes the top N tags with the most words. Defaults to None.
        topWordsPie (Optional[int], optional): Visualizes the top N most looked up words. Defaults to None.
        topTagsPie (Optional[int], optional): Visualizes the top N tags with the most words. Defaults to None.
        lookupWeek (Optional[bool], optional): Visualizes the word count distribution for days in the past week. Defaults to False.
        lookupMonth (Optional[bool], optional): Visualizes the word count distribution for days in the past month. Defaults to False.
        lookupYear (Optional[bool], optional): Visualizes the word count distribution for days in the past year. Defaults to False.
        learnVSmaster (Optional[bool], optional): Visualizes the number of words in your learning list vs. your mastered list. Defaults to False.
        slider (Optional[bool], optional): Shows all graphs one by one in a slider. Defaults to False.
    """
    from modules.Carousel import show_slider
    from modules.Graph import (
        viz_learning_vs_mastered,
        viz_top_tags_bar,
        viz_top_tags_pie,
        viz_top_words_bar,
        viz_top_words_pie,
        viz_word_distribution_category,
        viz_word_distribution_month,
        viz_word_distribution_week,
    )

    if topWordsBar:
        viz_top_words_bar(N=topWordsBar, popup=True)
    elif topTagsBar:
        viz_top_tags_bar(N=topTagsBar, popup=True)

    elif topWordsPie:
        viz_top_words_pie(popup=True)
    elif topTagsPie:
        viz_top_tags_pie(popup=True)

    elif lookupWeek:
        viz_word_distribution_week(popup=True)
    elif lookupMonth:
        viz_word_distribution_month(popup=True)

    elif learnVSmaster:
        viz_learning_vs_mastered(popup=True)

    elif wordCountByCollection:
        viz_word_distribution_category(popup=True)

    # by default, show all graphs in a GUI slider window
    else:
        # BUG 🐞 - slider will work as expected, after closing the termial will freeze up and not respond to any input
        show_slider()


@app.command(
    rich_help_panel="Text Processing & NLP",
    help="🧹 Filter out [b red1]Explicit[/b red1] words in a text or a webpage. Make it SFW!",
)
def clean(
    content: str = typer.Argument(..., help="🧹 Text or URL to [b red1]clean[/b red1]"),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="🧹 Completely [b red1]replace[/b red1] all bad words with asterisks.",
    ),
):

    from modules.NLP import censor_bad_words_not_strict, censor_bad_words_strict

    if strict:
        censor_bad_words_strict(content)
    else:
        censor_bad_words_not_strict(content)


@app.command(
    rich_help_panel="Text Processing & NLP",
    help="📝 Generate a [b orange_red1]Summary[/b orange_red1] of a text or a webpage.",
)
def summary(
    content: str = typer.Argument(
        ..., help="📝 Text or URL to [b orange_red1]summarize[/b orange_red1]"
    ),
    file: bool = typer.Option(
        False,
        "--file",
        "-f",
        help="📝 [b green]Save[/b green] the summary to a text file.",
    ),
):

    from modules.NLP import summarize_text

    if file:
        summarize_text(content, file=True)
    else:
        summarize_text(content)


@app.command(
    rich_help_panel="Text Processing & NLP",
    help="😯 Extract [b deep_pink2]Difficult[/b deep_pink2] Words from a text or a webpage.",
)
def hardwords(
    content: str = typer.Argument(
        ...,
        help="😯 Text or URL to extract [b deep_pink2]difficult words[/b deep_pink2] from",
    ),
):
    from modules.NLP import extract_difficult_words

    extract_difficult_words(content)


@app.command(
    rich_help_panel="Text Processing & NLP",
    help="😀😐😞 Get the [b dodger_blue3]Sentiment Analysis[/b dodger_blue3] of a text or a webpage.",
)
def sentiment(
    content: str = typer.Argument(
        ...,
        help="😀😐😞 Text or URL to get [b dodger_blue3]sentiment analysis[/b dodger_blue3] from",
    ),
):
    from modules.NLP import sentiment_analysis

    sentiment_analysis(content)


@app.command(
    rich_help_panel="Text Processing & NLP",
    help="💯 Get [b plum3]Readability Score[/b plum3] of a text or a webpage.",
)
def readability(
    content: str = typer.Argument(
        ..., help="💯 Text or URL to get [b plum3]readability score[/b plum3] from"
    ),
):
    from modules.NLP import readability_index

    readability_index(content)


@app.command(
    rich_help_panel="Miscellaneous",
    help="📰 Add, View or Delete [b green4]RSS[/b green4] feeds",
)
def rss(
    add: str = typer.Option(
        None, "--add", "-a", help="📰 [b green]Add[/b green] a new RSS feed."
    ),
    list: bool = typer.Option(
        False, "--list", "-l", help="📰 [b blue]View[/b blue] all RSS feeds."
    ),
    delete: bool = typer.Option(
        False, "--delete", "-d", help="📰 [b red]Delete[/b red] an RSS feed."
    ),
    read: str = typer.Option(
        None, "--read", "-r", help="📰 [b violet]Read[/b violet] an RSS feed."
    ),
):

    from modules.RSS import (
        add_feed,
        check_feed_for_new_content,
        get_all_feeds,
        remove_feed,
    )

    if add:
        add_feed(url=add)
    elif list:
        get_all_feeds()
    elif delete:
        remove_feed()
    elif read:
        check_feed_for_new_content(title=read)
    else:
        typer.echo("🤷 No option selected. Please select an option to continue.")


@app.command(
    rich_help_panel="Miscellaneous", help="✍🏼 Add, View, Search or Delete Delete Quotes"
)
def quote(
    random: bool = typer.Option(
        False, "--random", "-r", help="✍🏼 Show a random quote from the saved list."
    ),
    list: bool = typer.Option(
        False, "--list", "-l", help="✍🏼 Display all saved quotes."
    ),
    delete: bool = typer.Option(
        False, "--delete", "-d", help="✍🏼 Delete a quote from the saved list."
    ),
    add: bool = typer.Option(False, "--add", "-a", help="✍🏼 Add a new quote."),
    search: str = typer.Option(None, "--search", "-S", help="✍🏼 Search for a quote."),
    delete_all: bool = typer.Option(
        False, "--delete-all", "-D", help="✍🏼 Delete all quotes."
    ),
):

    from modules.Quotes import (
        add_quote,
        delete_all_quotes,
        delete_quote,
        get_quotes,
        get_random_quote,
        search_quote,
    )

    if random:
        get_random_quote()
    elif list:
        get_quotes()
    elif search:
        search_quote(quoteText=search)
    elif delete:
        delete_quote()
    elif delete_all:
        delete_all_quotes()
    elif add:
        print(Panel("📝 Enter the quote to add."))
        my_quote = typer.prompt("")
        print(Panel("Do you want to add the author of the quote? (y/n)"))

        if typer.confirm(""):
            print(Panel("📝 Enter the author of the quote. (Optional)"))
            my_author = typer.prompt("")
            add_quote(quote=my_quote, author=my_author)
        else:
            add_quote(quote=my_quote)


@app.command(
    rich_help_panel="Stats", help="🔥 Get the streak of days you have looked up words."
)
def streak():

    from modules.Utils import show_streak

    show_streak()


@app.command(
    rich_help_panel="Stats",
    help="🎯 Predict the milestone of words looked up via the app.",
)
def milestone(
    milestone_number: int = typer.Argument(
        ..., help="🎯 Number of words that marks a milestone."
    ),
):
    from modules.Utils import predict_milestone

    predict_milestone(milestone_number)


@app.command(rich_help_panel="Miscellaneous", help="🔆 Get quote of the day.")
def daily_quote():
    from modules.Quotes import get_quote_of_the_day

    get_quote_of_the_day()


@app.command(rich_help_panel="Miscellaneous", help="😍 Get word of the day.")
def daily_word():
    from modules.Dictionary import get_word_of_the_day

    get_word_of_the_day()


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="🎫 Generate flashcards for words in your learning list",
)
def flashcard(
    all: bool = typer.Option(False, "--all", "-a", help="🎫 Generate for all words."),
    learning: bool = typer.Option(
        False, "--learning", "-l", help="🎫 Generate for words set as learning."
    ),
    mastered: bool = typer.Option(
        False, "--mastered", "-m", help="🎫 Generate for words set as mastered."
    ),
    favorite: bool = typer.Option(
        False, "--favorite", "-f", help="🎫 Generate for words set as favorite."
    ),
    tag: str = typer.Option(
        None, "--tag", "-t", help="🎫 Generate for words with a specific tag."
    ),
):

    """
    Create flashcards for words in your learning list.
    """

    from modules.Flashcard import (
        generate_all_flashcards,
        generate_favorite_flashcards,
        generate_learning_flashcards,
        generate_mastered_flashcards,
        generate_tag_flashcards,
    )

    if all:
        generate_all_flashcards()
    elif learning:
        generate_learning_flashcards()
    elif mastered:
        generate_mastered_flashcards()
    elif favorite:
        generate_favorite_flashcards()
    elif tag:
        generate_tag_flashcards(tag)
    else:
        print(Panel("Cannot combine options. Please select only one option."))


@app.command(
    rich_help_panel="Vocabulary Builder",
    help="🔠 Spell check your input sentences and find the misspelled words.",
)
def spellcheck(text: str = typer.Argument(..., help="🔠 Text to spell check.")):
    """
    Spell check a word.
    """

    from modules.Spelling import spell_checker

    spell_checker(text)


if __name__ == "__main__":
    from modules.Database import initializeDB
    from modules.WordCollections import (
        clean_collection_csv_data,
        delete_collection_from_DB,
        insert_collection_to_DB,
    )

    # check if Vocabulary.db exists, if not create it
    if not os.path.exists("VocabularyBuilder.db"):

        # initialize the database with the tables if not already existing
        initializeDB()
        # uncomment this to easily delete all words from collections table during testing
        delete_collection_from_DB()
        clean_collection_csv_data()
        # add all the collection words to the database if not already existing
        insert_collection_to_DB()

    app()
