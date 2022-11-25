import typer
import sys
from typing import *
from rich import print
from rich.console import Console
from modules.Dictionary import (definition, say_aloud)
from modules.Database import initializeDB
from modules.Banner import print_banner
from modules.Utils import *
from modules.ImportExport import *

# app configuration
app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=False,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)

# TODO : find a way to print the banner only once when the app is launched. Currently it is printed everytime a command is executed.
console = Console(record=False, color_system="truecolor")
print_banner(console)   

# initialize the database with the tables if not already existing
initializeDB()


@app.command(rich_help_panel="Options", help="📚 [bold red]Exits[/bold red] the CLI")
def bye():
    print(Panel(":wave: [bold green]Bye bye![/bold green]"))
    sys.exit(0)


@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    words: List[str] = typer.Argument(..., help="Word to search"),
    short: Optional[bool] = typer.Option(False, "--short", "-s", help="Lightweight definitions."),
    pronounce: Optional[bool] = typer.Option(False, "--pronounce",  "-p", help="Pronounce the word."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag the word in your vocabulary builder set.")
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
            
        if tag:
            add_tag(word, tag)
        
        if not tag:
            add_tag(word)
    


# todo @anay: add a command to show word list [either all or by tag or by date or by learning/mastered]
# todo @anay: PyTest for this
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold blue]Lists [/bold blue] of all your looked up words")
def list(
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Get a list of your favorite words."),
    learning: Optional[bool] = typer.Option(False, "--learning",  "-l", help="Get a list of words in your learning list."),
    mastered: Optional[bool] = typer.Option(None, "--mastered", "-m", help="Get a list of words in your mastered list."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Get a list of words with a particular tag."),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Get a list of words from a particular date."),
    last: Optional[str] = typer.Option(10, "--last", "-L", help="Get a list of last searched words."),
    most: Optional[str] = typer.Option(10, "--most", "-M", help="Get a list of most searched words."),
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
    else:
        # show all the words by default
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

 
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Delete[/bold red] words from your lists")
def delete(
    words:List[str] = typer.Argument(..., help="Words to delete from your lists"),
    ):
    for word in words:
        delete_word(word)
        
        
@app.command(rich_help_panel="Vocabulary Builder", help="📝 [bold red]Clears[/bold red] all lists")        
def clear(
    all: Optional[bool] = typer.Option(False, "--all", "-a", help="Clear all words in all lists"),
    learning: Optional[bool] = typer.Option(False, "--learning", "-l", help="Clear all words in your learning list"),
    master: Optional[bool]= typer.Option(False, "--mastered", "-m", help="Clear all words in your mastered list"),
    favorite: Optional[bool] = typer.Option(False, "--favorite", "-f", help="Clear all words in your favorite list"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Clear all words with a particular tag"),
):
    if all:
        delete_all()
    if learning:
        delete_learning()
    if master:
        delete_mastered()
    if favorite:
        delete_favorite()
    if tag:
        delete_words_from_tag(tag)
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
    tag: str = typer.Argument(..., help="Tag to add to the words"), #is str right or should it be a list? And can we add multiple tags to a single word? @atharva
):
    for word in words:
        add_tag(word, tag)


# todo @anay: add a command to untag a word   ✅
@app.command(rich_help_panel="Vocabulary Builder", help="📚 [bold red]Remove[/bold red] tag of a word in the dictionary")
def untag(
    words: List[str] = typer.Argument(..., help="Word to remove tag from"),
    tag: str = typer.Argument(None, "--untag", "-u", help="Tag which is to be removed from the word"), #is this right or flags should be removed as it is a compulsory argument @atharva
):  
    for word in words:
        remove_tag(word, tag)


# todo @atharva: add a command "about" to get software details. Banner, version, credits


# todo @atharva: add a command to get learning rate of the user
# OPTIONS/FLAGS will be (two or more can be used at once):
# --today: get learning rate today
# --week: get learning rate this week
# --month: get learning rate this month
# --year: get learning rate this year
# --graph: get learning rate graph


# todo @atharva: add a command to export flashcards (images)
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag: export words of a particular tag

if __name__ == "__main__":
    app()
