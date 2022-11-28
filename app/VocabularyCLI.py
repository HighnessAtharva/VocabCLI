import typer
import sys
from typing import *
from rich import print
from rich.console import Console
from modules.Dictionary import (definition, say_aloud)
from modules.Database import initializeDB
from modules.Banner import print_banner
from modules.Utils import *
from modules.About import *
from modules.ImportExport import *
from modules.Thesaurus import *

# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=True,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)


# initialize the database with the tables if not already existing
initializeDB()


@app.command(rich_help_panel="Options", help="📚 [bold red]Exits[/bold red] the CLI")
def bye():
    print(Panel(":wave: [bold green]Bye bye![/bold green]"))
    sys.exit(0)

# todo add an flag to show examples
@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    words: List[str] = typer.Argument(..., help="Word to search"),
    short: Optional[bool] = typer.Option(False, "--short", "-s", help="Lightweight definitions."),
    pronounce: Optional[bool] = typer.Option(False, "--pronounce",  "-p", help="Pronounce the word."),
):
    """
    Shows the definition of WORD.
    Adds it to the vocabulary builder list along with the timestamp if the user is logged in.
    """

    for word in words:
        if short:
            definition(word, short=True)

        if not short:
            definition(word, short=False)

        if pronounce:
            say_aloud(query=word)





# todo @anay: add a command to show word list [either all or by tag or by date or by learning/mastered]
# todo @anay: PyTest for this
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold blue]Lists [/bold blue] of all your looked up words")
def list(
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Get a list of your favorite words."),
    learning: Optional[bool] = typer.Option(False, "--learning",  "-l", help="Get a list of words in your learning list."),
    mastered: Optional[bool] = typer.Option(None, "--mastered", "-m", help="Get a list of words in your mastered list."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Get a list of words with a particular tag."),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Get a list of words from a particular date."),
    last: Optional[str] = typer.Option(None, "--last", "-L", help="Get a list of last searched words."),
    most: Optional[str] = typer.Option(None, "--most", "-M", help="Get a list of most searched words."),
    tagnames: Optional[bool] = typer.Option(False, "--tagnames", "-T", help="Get a list of all the tags."),
):

    if favorite:
        show_list(favorite=True)
    if learning:
        show_list(learning=True)
    if mastered:
        show_list(mastered=True)
    if tag:
        show_list(tag=tag)
    if date:
        show_list(date=date)
    if last:
        show_list(last=last)
    if most:
        show_list(most=most)
    # todo: PyTest pending for this
    if tagnames:
        show_list(tagnames=True)
    elif not any([favorite, learning, mastered, tag, date, last, most]):
        show_list()


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold green]Sets[/bold green] a word as [bold gold1]favorite[/bold gold1]")
def favorite(
    words: List[str] = typer.Argument(..., help="Word to add to favorites."),
):
    for word in words:
        set_favorite(word)


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Removes[/bold red] the word from [bold gold1]favorites[/bold gold1]")
def unfavorite(
    words: List[str] = typer.Argument(..., help="Word to remove from favorites"),
):
    for word in words:
        set_unfavorite(word)


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold green]Sets[/bold green] a word as [bold blue]learning[/bold blue]")
def learn(
    words: List[str] = typer.Argument(..., help="Word to add to learning."),
):
    for word in words:
        set_learning(word)


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Removes[/bold red] the word from [bold blue]learning[/bold blue]")
def unlearn(
    words: List[str] = typer.Argument(..., help="Word to remove from learning"),
):
    for word in words:
        set_unlearning(word)


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold green]Sets[/bold green] a word as [bold green]mastered[/bold green]")
def master(
    words: List[str] = typer.Argument(..., help="Word to add to mastered."),
):
    for word in words:
        set_mastered(word)


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Removes[/bold red] the word from [bold green]mastered[/bold green]")
def unmaster(
    words: List[str] = typer.Argument(..., help="Word to remove from mastered"),
):
    for word in words:
        set_unmastered(word)

# todo - change the test to take care of the confirmation prompt
# todo @anay: manually test this once. Have added a confirmation prompt
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Delete[/bold red] words from your lists")
def delete(
    words:List[str] = typer.Argument(..., help="Words to delete from your lists"),
    ):
    if len(words)==1:
        sure = typer.confirm(f"Are you sure you want to delete '{words[0]}'?")
    else:
        sure = typer.confirm(f"Are you sure you want to delete {len(words)} words?")
    if sure:
        for word in words:
            delete_word(word)
    else:
        print("Ok, not deleting anything.")


# todo - change the test to take care of the confirmation prompt
# todo @anay: manually test this once. Have added a confirmation prompt
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Clears[/bold red] all lists")
def clear(
    all: Optional[bool] = typer.Option(False, "--all", "-a", help="Clear all words in all lists"),
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Clear all words in your learning list"),
    master: Optional[bool]= typer.Option(False, "--mastered", "-m", help="Clear all words in your mastered list"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Clear all words in your favorite list"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Clear all words with a particular tag"),
):
    if all:
        print("🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words in all lists?[/b]")
        if sure := typer.confirm(""):
            delete_all()
        else:
            print("OK, not deleting anything.")

    elif learning:
        print("🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your learning list[/b]?")
        if sure := typer.confirm(""):
            delete_learning()
        else:
            print("OK, not deleting anything.")

    elif master:
        print("🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your mastered list[/b]?")
        if sure := typer.confirm(""):
            delete_mastered()
        else:
            print("OK, not deleting anything.")

    elif favorite:
        print("🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your favorite list[/b]?")
        if sure := typer.confirm(""):
            delete_favorite()
        else:
            print("OK, not deleting anything.")

    elif tag:
        print("🛑 [bold red]DANGER[/bold red] Are you sure you want to clear [b]all words from your favorite list[/b]?")
        if sure := typer.confirm(""):
            delete_words_from_tag(tag)
        else:
            print("OK, not deleting anything.")

    else:
        print(Panel("[bold red] you cannot combine options with clear command[/bold red] ❌"))


@app.command(rich_help_panel="Import / Export", help="📝 [bold blue]Exports[/bold blue] a list of all your looked up words")
def export(
    pdf: Optional[bool] = typer.Option(False, "--pdf", "-P", help="Export a list of your looked up words in PDF format."),
):
    if pdf:
        export_to_pdf()
    else:
        export_to_csv()


@app.command("import", rich_help_panel="Import / Export", help="📝 [bold blue]Imports[/bold blue] a list words in the application")
def Import():
    import_from_csv()


@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold blue]Tags[/bold blue] a word")
def tag(
    words: List[str] = typer.Argument(..., help="Words to tagged"),
    tag: str = typer.Option(..., "--name", "-n", help="Tag to add to the words"),
):
    for word in words:
        add_tag(word, tag)


@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold red]Remove[/bold red] tag of a word in the dictionary")
def untag(
    words: List[str] = typer.Argument(..., help="Word to remove tag from"),
):
    for word in words:
        remove_tag(word)


@app.command(rich_help_panel="About", help="📚 [bold blue]About[/bold blue] the software")
def about():
    console = Console(record=False, color_system="truecolor")
    print_banner(console)
    print_about_app()

# todo conditionals need to be fixed
@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold blue]Learning Rate[/bold blue] gives the number of words you have learned in a particular time period with a comparison of a previous time period")
def rate(
    today: Optional[bool] = typer.Option(False, "--today", "-t", help="Get learning rate today"),
    week: Optional[bool] = typer.Option(False, "--week", "-w", help="Get learning rate this week"),
    month: Optional[bool] = typer.Option(False, "--month", "-m", help="Get learning rate this month"),
    year: Optional[bool] = typer.Option(False, "--year", "-y", help="Get learning rate this year"),

):
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




# todo @atharva: add a command to export flashcards (images)
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag: export words of a particular tag

# todo revise

# todo homophones

# todo synonyms
@app.command(rich_help_panel="Thesaurus", help="📚 Find [bold pink]synonyms[/bold pink] for a word")
def synonym(
    words: List[str] = typer.Argument(..., help="Word to search synonyms for"),
):
    for word in words:
        find_synonym(word)

# todo antonyms
@app.command(rich_help_panel="Thesaurus", help="📚 Find [bold pink]antonyms[/bold pink] for a word")
def antonym(
    words: List[str] = typer.Argument(..., help="Word to search antonyms for"),
):
    for word in words:
        find_antonym(word)


# todo: SPACY: paraphrase

# todo: SPACY: sentiment analysis

# todo: SPACY: check paraphrase

if __name__ == "__main__":
    app()
