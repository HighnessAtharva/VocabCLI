from modules.About import *
from modules.Banner import print_banner
from modules.Database import *
from modules.Dictionary import definition, say_aloud
from modules.ImportExport import *
from modules.Study import *
from modules.Thesaurus import *
from modules.Utils import *
from modules.Graph import *
from modules.Flashcard import *
from modules.WordCollections import *
from modules.Carousel import *
from modules.NLP import *
from modules.RSS import *
from modules.Quotes import *
import sys
import pyperclip
import typer
from typing import *
from rich import print
from rich.console import Console
from datetime import datetime
from spellchecker import SpellChecker


# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=False,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)


@app.command(rich_help_panel="Miscellaneous", help="👋🏼 [bold red]Exits[/bold red] the CLI")
def bye():
    print(Panel(":wave: [bold green]Bye bye![/bold green]"))
    sys.exit(0)


@app.command(rich_help_panel="Miscellaneous", help="🔄 Update the JSON response in the cache")
def refresh():
    """
    Refreshes the cached content from the API.
    """
    refresh_cache()


@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    words: List[str] = typer.Argument(..., help="Word to search"),
    short: bool = typer.Option(False, "--short", "-s", help="Lightweight definitions."),
    pronounce: bool = typer.Option(False, "--pronounce",  "-p", help="Pronounce the word."),
):  # sourcery skip: use-named-expression
    """
    Looks up a word in the dictionary.

    Args:
        words (List[str]): Word which is to be defined.
        short (bool, optional): If True, prints the short definition of the word. Defaults to False.
        pronounce (bool, optional): If True, plays the pronunciation of the word. Defaults to False.
    """

    spell=SpellChecker()    
    for word in words:
        
        # check if the word is mispelled
        mispelled = spell.unknown([word])
        if mispelled:
            # store other possible correct words
            for x in mispelled:
                candidates=spell.candidates(x)
                # if there are other possible correct words then ask the user if they meant any of them
                if candidates:
                    candidates = ', '.join(candidates)
                    print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                            title_align="center",
                            padding=(1, 1),
                            renderable=f"The word {word} was not found. Did you mean [u blue]{candidates}[/u blue]? 🤔")
                    )
                    break
                
                # otherwise, print the word unavailable message
                else:
                    print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                            title_align="center",
                            padding=(1, 1),
                            renderable=f"The word [bold red]{word}[/bold red] is not a valid word. Please check the spelling. 🤔")
                    )

        else:
            if short:
                definition(word, short=True)

            if not short:
                definition(word, short=False)

            if pronounce:
                say_aloud(query=word)
     
            



@app.command("list", rich_help_panel="Word Management", help="📝 [bold blue]Lists [/bold blue] of all your looked up words")
def ListCMD(
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Get a list of your favorite words."),
    learning: bool = typer.Option(False, "--learning",  "-l", help="Get a list of words in your learning list."),
    mastered: bool = typer.Option(None, "--mastered", "-m", help="Get a list of words in your mastered list."),
    tag: str = typer.Option(None, "--tag", "-t", help="Get a list of words with a particular tag."),
    days: int = typer.Option(None, "--days", "-d", help="Get a list of words from last n number of days."),
    date: bool = typer.Option(False, "--date", "-D", help="Get a list of words from a particular date."),
    last: int = typer.Option(None, "--last", "-L", help="Get a list of last searched words."),
    most: int = typer.Option(None, "--most", "-M", help="Get a list of most searched words."),
    tags: bool = typer.Option(False, "--tagnames", "-T", help="Get a list of all the tags."),
    collection: str = typer.Option(None, "--collection", "-c", help="Get a list of words from a collection."),
    collections: bool = typer.Option(False, "--collections", "-C", help="Get a list of all the collections."),
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
        
    elif not any([favorite, learning, mastered, tag, days, date, last, most, collection, collections, tags]):
        show_list()


@app.command(rich_help_panel="Word Management", help="💙 [bold green]Sets[/bold green] a word as [bold gold1]favorite[/bold gold1]")
def favorite(
    words: List[str] = typer.Argument(..., help="Word to add to favorites."),
):
    """
    Adds a word to the favorite list.

    Args:
        words (List[str]): Word which is to be added to the favorite list.
    """

    for word in words:
        set_favorite(word)


@app.command(rich_help_panel="Word Management", help="💔 [bold red]Removes[/bold red] the word from [bold gold1]favorites[/bold gold1]")
def unfavorite(
    words: List[str] = typer.Argument(..., help="Word to remove from favorites"),
):
    """
    Removes a word from the favorite list.

    Args:
        words (List[str]): Word which is to be removed from the favorite list.
    """

    for word in words:
        set_unfavorite(word)


@app.command(rich_help_panel="Word Management", help="✍🏼 [bold green]Sets[/bold green] a word as [bold blue]learning[/bold blue]")
def learn(
    words: List[str] = typer.Argument(..., help="Word to add to learning."),
):
    """
    Adds a word to the learning list.

    Args:
        words (List[str]): Word which is to be added to the learning list.
    """

    for word in words:
        set_learning(word)


@app.command(rich_help_panel="Word Management", help="😪 [bold red]Removes[/bold red] the word from [bold blue]learning[/bold blue]")
def unlearn(
    words: List[str] = typer.Argument(..., help="Word to remove from learning"),
):
    """
    Removes a word from the learning list.

    Args:
        words (List[str]): Word which is to be removed from the learning list.
    """

    for word in words:
        set_unlearning(word)


@app.command(rich_help_panel="Word Management", help="🧠 [bold green]Sets[/bold green] a word as [bold green]mastered[/bold green]")
def master(
    words: List[str] = typer.Argument(..., help="Word to add to mastered."),
):
    """
    Adds a word to the mastered list.

    Args:
        words (List[str]): Word which is to be added to the mastered list.
    """

    for word in words:
        set_mastered(word)


@app.command(rich_help_panel="Word Management", help="🤔 [bold red]Removes[/bold red] the word from [bold green]mastered[/bold green]")
def unmaster(
    words: List[str] = typer.Argument(..., help="Word to remove from mastered"),
):
    """
    Removes a word from the mastered list.

    Args:
        words (List[str]): Word which is to be removed from the mastered list.
    """

    for word in words:
        set_unmastered(word)


@app.command(rich_help_panel="Import & Export", help="📂 [bold blue]Exports[/bold blue] a list of all your looked up words")
def export(
    pdf: bool = typer.Option(False, "--pdf", "-P", help="Export a list of your looked up words in PDF format."),
):
    """
    Exports a list of all your looked up words.

    Args:
        pdf (bool, optional): If True, exports a list of your looked up words in PDF format. Defaults to False.
    """

    if pdf:
        export_to_pdf()
    else:
        export_to_csv()


@app.command("import", rich_help_panel="Import & Export", help="🔼 [bold blue]Imports[/bold blue] a list words in the application")
def Import():
    """
    Imports a list of words in the application.
    """

    import_from_csv()


@app.command(rich_help_panel="Word Management", help="🔖 [bold blue]Tags[/bold blue] a word")
def tag(
    words: List[str] = typer.Argument(..., help="Words to tagged"),
    tag: str = typer.Option(..., "--name", "-n", help="Tag to add to the words"),
):
    """
    Tags a word.

    Args:
        words (List[str]): Words to tagged.
        tag (str): Tag to add to the words.
    """

    for word in words:
        add_tag(word, tag)


@app.command(rich_help_panel="Word Management", help="✂ [bold red] Removes[/bold red] tag of a word in the dictionary")
def untag(
    words: List[str] = typer.Argument(..., help="Word to remove tag from"),
):
    """
    Remove tag of a word in the dictionary.

    Args:
        words (List[str]): Word to remove tag from.
    """

    for word in words:
        remove_tag(word)


@app.command(rich_help_panel="Miscellaneous", help="💻 [bold blue]About[/bold blue] the software")
def about():
    """
    Print information about the software.
    """

    console = Console(record=False, color_system="truecolor")
    print_banner(console)
    print_about_app()


@app.command(rich_help_panel="Vocabulary Builder", help="📊 [bold blue]Learning Rate[/bold blue] gives the number of words you have learned in a particular time period with a comparison of a previous time period")
def rate(
    today: bool = typer.Option(False, "--today", "-t", help="Get learning rate today"),
    week: bool = typer.Option(False, "--week", "-w", help="Get learning rate this week"),
    month: bool = typer.Option(False, "--month", "-m", help="Get learning rate this month"),
    year: bool = typer.Option(False, "--year", "-y", help="Get learning rate this year"),
):
    """
    Gives the number of words you have learned in a particular time period with a comparison of a previous time period.

    Args:
        today (bool, optional): If True, get learning rate today. Defaults to False.
        week (bool, optional): If True, get learning rate this week. Defaults to False.
        month (bool, optional): If True, get learning rate this month. Defaults to False.
        year (bool, optional): If True, get learning rate this year. Defaults to False.
    """

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



@app.command(rich_help_panel="Vocabulary Builder", help="🔎 Find [bold pink]synonyms[/bold pink] for a word")
def synonym(
    words: List[str] = typer.Argument(..., help="Word to search synonyms for"),
):
    """
    Find synonyms for a word.

    Args:
        words (List[str]): Word to search synonyms for.
    """

    for word in words:
        find_synonym(word)


@app.command(rich_help_panel="Vocabulary Builder", help="❌ Find [bold pink]antonyms[/bold pink] for a word")
def antonym(
    words: List[str] = typer.Argument(..., help="Word to search antonyms for"),
):
    """
    Find antonyms for a word.

    Args:
        words (List[str]): Word to search antonyms for.
    """

    for word in words:
        find_antonym(word)


@app.command(rich_help_panel="Vocabulary Builder", help="🔁 Get a lookup history of a word")
def history(
    words: List[str] = typer.Argument(..., help="Word to get lookup history for"),
):
    """
    Get a lookup history of a word.

    Args:
        words (List[str]): Word to get lookup history for.
    """

    for word in words:
        fetch_word_history(word)


@app.command(rich_help_panel="Word Management", help="🚮 Deletes the word from the database")
def delete(
    mastered: bool = typer.Option(False, "--mastered", "-m", help="Deletes all mastered words"),
    learning: bool = typer.Option(False, "--learning", "-l", help="Deletes all learning words"),
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Deletes all favorite words"),
    tag: str = typer.Option(None, "--tag", "-t", help="Tag of words to be deleted"),
    words: List[str] = typer.Argument(None, help="Word to be deleted"),
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


    if mastered:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your mastered list[/b]?")
        )

        if sure := typer.confirm(""):
            delete_mastered()
        else:
            print(Panel("OK, not deleting anything."))

    elif learning:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your learning list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_learning()
        else:
            print(Panel("OK, not deleting anything."))

    elif favorite:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your favorite list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_favorite()
        else:
            print(Panel("OK, not deleting anything."))

    elif tag:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from tag {tag}[/b]?")
        )
        if sure := typer.confirm(""):
            delete_words_from_tag(tag)
        else:
            print(Panel("OK, not deleting anything."))

    elif words:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to delete these [b]{len(words)} words from your list[/b]?")
        )
        if sure := typer.confirm(""):
            for word in words:
                delete_word(word)
        else:
            print(Panel("OK, not deleting anything."))

    elif not any([mastered, learning, favorite, tag, words]):
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to delete [b]all words from your list[/b]?")
        )
        if sure := typer.confirm(""):
            delete_all()
        else:
            print(Panel("OK, not deleting anything."))


@app.command(rich_help_panel="Word Management", help="🧹 [bold red]Clears[/bold red] all lists")
def clear(
    learning: bool = typer.Option(False, "--learning", "-l", help="Clear all words in your learning list"),
    master: bool= typer.Option(False, "--mastered", "-m", help="Clear all words in your mastered list"),
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Clear all words in your favorite list"),
    tag: str = typer.Option(None, "--tag", "-t", help="Clear all words with a particular tag"),
):
    """
    Clears all the words from the lists.

    Args:
        learning (bool, optional): If True, clears all the words from the learning list. Defaults to False.
        master (bool, optional): If True, clears all the words from the mastered list. Defaults to False.
        favorite (bool, optional): If True, clears all the words from the favorite list. Defaults to False.
        tag (str, optional): If True, clears all the words with a particular tag. Defaults to None.
    """

    if learning:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your learning list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_learning()
        else:
            print(Panel("OK, not clearing anything."))

    elif master:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your mastered list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_mastered()
        else:
            print(Panel("OK, not clearing anything."))

    elif favorite:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your favorite list[/b]?")
        )
        if sure := typer.confirm(""):
            clear_favorite()
        else:
            print(Panel("OK, not clearing anything."))

    elif tag:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your tag {tag}[/b]?")
        )
        if sure := typer.confirm(""):
            clear_all_words_from_tag(tag)
        else:
            print(Panel(f"OK, not learning any words from the tag {tag}."))
    
    else:
        raise typer.BadParameter(message="Please specify a list to clear. Use --help for more info.")


# TODO: - add more flags/options
@app.command(rich_help_panel="Vocabulary Builder", help="🔀 Gets a random word")
def random(
    learning: bool = typer.Option(False, "--learning", "-l", help="Get a random learning word"),
    mastered: bool = typer.Option(False, "--mastered", "-m", help="Get a random mastered word"),
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Get a random favorite word"),
    tag: str = typer.Option(None, "--tag", "-t", help="Get a random word from a particular tag"),
    collection: str = typer.Option(None, "--collection", "-c", help="Get a random word from a particular collection"),
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


@app.command(rich_help_panel="Vocabulary Builder", help="💡 Revise words from your learning list")
def revise(
    number: int = typer.Option(None, "--number", "-n", help="Number of words to revise in random order."),
    tag: str = typer.Option(None, "--tag", "-t", help="Revise words in a particular tag."),
    learning: bool = typer.Option(False, "--learning", "-l", help="Revise words in your learning list"),
    mastered: bool = typer.Option(False, "--mastered", "-m", help="Revise words in your mastered list"),
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Revise words in your favorite list"),
    collection: str = typer.Option(None, "--collection", "-c", help="Revise words in a particular collection")
):  # sourcery skip: remove-redundant-if
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
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="Cannot combine these arguments")
        ) 
        
# TODO: - need to find a way to force break out of the quiz using Ctrl+C, currently it only aborts the current word
@app.command(rich_help_panel="Vocabulary Builder", help="❓ Take a quiz on words in your learning list")
def quiz(
    number: int = typer.Option(None, "--number", "-n", help="Limit the number of words to quiz on.", min=4),
    tag: str = typer.Option(None, "--tag", "-t", help="Tag of words to quiz on."),
    learning: bool = typer.Option(False, "--learning", "-l", help="Take a quiz on words in your learning list"),
    mastered: bool = typer.Option(False, "--mastered", "-m", help="Take a quiz on words in your mastered list"),
    favorite: bool = typer.Option(False, "--favorite", "-f", help="Take a quiz on words in your favorite list"),
    collection: str = typer.Option(None, "--collection", "-c", help="Take a quiz on words in a particular collection"),
    history: bool = typer.Option(False, "--history", "-h", help="Show quiz history and stats")
):  # sourcery skip: remove-redundant-if
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
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="Cannot combine these arguments")
        ) 

@app.command(rich_help_panel="Stats", help="📚 Generate Graphical Charts based on your vocabulary")
def graph(
    topWordsBar: int = typer.Option(None, "--topwordsbar", "-twb", help="Bar Graph of Top N Most Looked Up Words", max=25, min=1),
    topTagsBar: int = typer.Option(None, "--toptagsbar", "-ttb", help="Bar Graph of Top N Tags with the most words.", max=25, min=1),
    
    topWordsPie: bool = typer.Option(False, "--topwordspie", "-twp", help="Pie Chart of Top 10 Most Looked Up Words"),
    topTagsPie: bool = typer.Option(False, "--toptagspie", "-ttp", help="Pie Chart of Top 10 Tags with the most words."),
    
    lookupWeek: bool = typer.Option(False, "--lookupweek", "-lw", help="Bar Graph of the word count distribution for days in the past week."),
    lookupMonth: bool = typer.Option(False, "--lookupmonth", "-lm", help="Bar Graph of the word count distribution for days in the past month."),
    lookupYear: bool = typer.Option(False, "--lookupyear", "-ly", help="Bar Graph of the word count distribution for days in the past year."),
    
    learnVSmaster: bool = typer.Option(False, "--learnvsmaster", "-lvm", help="Stacked Graph the number of words in your learning list vs. your mastered list."),
    
    wordCountByCollection: bool = typer.Option(False, "--wordcategories", "-wc", help="Bar Graph of the number of words in a category domain."),
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
        
    if topWordsBar:
        viz_top_words_bar(N=topWordsBar, popup=True)
    elif topTagsBar:
        viz_top_tags_bar(N=topTagsBar,popup=True)
    
    elif topWordsPie:
        viz_top_words_pie(popup=True)
    elif topTagsPie:
        viz_top_tags_pie(popup=True)
    
    elif lookupWeek:
        viz_word_distribution_week(popup=True)
    elif lookupMonth:
        viz_word_distribution_month(popup=True)
    elif lookupYear:
        viz_word_distribution_year(popup=True)
    
    elif learnVSmaster:
        viz_learning_vs_mastered(popup=True)
    
    elif wordCountByCollection:
        viz_word_distribution_category(popup=True)
    
    # by default, show all graphs in a GUI slider window
    else:
        # BUG 🐞 - slider will work as expected, after closing the termial will freeze up and not respond to any input 
        show_slider()



# TODO: - some testing required
@app.command(rich_help_panel="Text Processing & NLP", help="Filter out explicit words in a text or a webpage. Make it SFW!")
def clean(
    strict: bool = typer.Option(False, "--strict", "-s", help="Completely replace all bad words with asterisks."),
):
    check_clipboard=pyperclip.paste()
    if check_clipboard:
        if confirm := typer.confirm(
            "📋 Clipboard text detected. Do you want to paste the content?"
        ):
            text=check_clipboard
        else:
            text=typer.prompt("Enter Text or URL to clean")

    if not check_clipboard:
        text=typer.prompt("Enter Text or URL to clean")

    if strict:
        censor_bad_words_strict(text)
    else:
        censor_bad_words_not_strict(text)
        

# TODO: - not tested at all, manual testing necessary
@app.command(rich_help_panel="Text Processing & NLP", help="📝 Generate a summary of a text or a webpage.")
def summary(
    file: bool = typer.Option(False, "--file", "-f", help="Save the summary to a text file."),
):
    check_clipboard=pyperclip.paste()
    if check_clipboard:
        if confirm := typer.confirm(
            "📋 Clipboard text detected. Do you want to paste the content?"
        ):
            text=check_clipboard

        else:
            text=typer.prompt("Enter Text or URL to summarize")

    if not check_clipboard:
        text=typer.prompt("Enter Text or URL to summarize")
    if file:
        summarize_text(text, file=True)
    else:
        summarize_text(text)
        
# TODO: - not tested at all, manual testing necessary
@app.command(rich_help_panel="Text Processing & NLP", help="📝 Extract Difficult Words from a text or a webpage.")
def hardwords():
    if check_clipboard := pyperclip.paste():
        if confirm := typer.confirm(
            "📋 Clipboard text detected. Do you want to paste the content?"
        ):
            text=check_clipboard

        else:
            text=typer.prompt("Enter Text or URL to extract difficult words")
        
    if not check_clipboard:
        text=typer.prompt("Enter Text or URL to extract difficult words")
    extract_difficult_words(text)
    
    
# TODO: - not tested at all, manual testing necessary
@app.command(rich_help_panel="Text Processing & NLP", help="📝 Get the Sentiment Analysis of a text or a webpage.")
def sentiment():
    check_clipboard=pyperclip.paste()
    if check_clipboard:
        if confirm := typer.confirm(
            "📋 Clipboard text detected. Do you want to paste the content?"
        ):
            text=check_clipboard

        else:
            text=typer.prompt("Enter Text or URL to get the sentiment analysis")

    if not check_clipboard:
        text=typer.prompt("Enter Text or URL to get the sentiment analysis")

    sentiment_analysis(text)
    
@app.command(rich_help_panel="Text Processing & NLP", help="📝 Get readability score of a text or a webpage.")
def readability():
    if check_clipboard := pyperclip.paste():
        if confirm := typer.confirm(
            "📋 Clipboard text detected. Do you want to paste the content?"
        ):
            text=check_clipboard

        else:
            text=typer.prompt("Enter Text or URL to summarize")

    readability_index(text)


@app.command(rich_help_panel="Miscellaneous", help="📝 Add, View or Delete RSS feeds")
def rss(
    add: str = typer.Option(None, "--add", "-a", help="Add a new RSS feed."),
    list: bool = typer.Option(False, "--list", "-l", help="View all RSS feeds."),
    delete: bool = typer.Option(False, "--delete", "-d", help="Delete an RSS feed."),
    read: str = typer.Option(None, "--read", "-r", help="Read an RSS feed."),
):
    if add:
        add_feed(url=add)
    elif list:
        get_all_feeds()
    elif delete:
        remove_feed()
    elif read:
        check_feed_for_new_content(title=read)
    else:
        typer.echo("🤷‍♀️ No option selected. Please select an option to continue.")


@app.command(rich_help_panel="Miscellaneous", help="📝 Add, View, Search or Delete Delete Quotes")
def quote(
    random: bool = typer.Option(False, "--random", "-r", help="Show a random quote from the saved list."),
    list: bool = typer.Option(False, "--list", "-l", help="Display all saved quotes."),
    delete: bool = typer.Option(False, "--delete", "-d", help="Delete a quote from the saved list."),
    add: bool = typer.Option(False, "--add", "-a", help="Add a new quote."),
    search: str = typer.Option(None, "--search", "-S", help="Search for a quote."),
    delete_all: bool = typer.Option(False, "--delete-all", "-D", help="Delete all quotes."),
):
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
        print("📝 Enter the quote to add.")
        my_quote=typer.prompt("")
        print("Do you want to add the author of the quote? (y/n)")
        
        if typer.confirm(""):
            print("📝 Enter the author of the quote. (Optional)")    
            my_author=typer.prompt("")
            add_quote(quote=my_quote, author=my_author)
        else:
            add_quote(quote=my_quote)
        
        
@app.command(rich_help_panel="Stats", help="📝Get the streak of days you have looked up words.")
def streak():
    show_streak()
    
    
@app.command(rich_help_panel="Stats", help="📝Predict the milestone of words looked up via the app.")
def milestone(
    milestone_number: int = typer.Argument(...,help="Number of words that marks a milestone."),
):
    predict_milestone(milestone_number)
    
@app.command("qotd", rich_help_panel="Miscellaneous", help="📝 Get quote of the day.")
def quote_of_the_day():
    get_quote_of_the_day()
    
# TODO: - need to write the function
@app.command(rich_help_panel="Vocabulary Builder", help="📇 Create flashcards for words in your learning list")
def flashcard():
    """
    Create flashcards for words in your learning list.
    """
    pass


  

if __name__ == "__main__":
    
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

    


