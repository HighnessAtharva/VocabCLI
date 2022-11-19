import typer
from typing import *
from rich import print
import Dictionary
import Database



# initialize the database with the tables if not already existing
Database.initializeDB()

app = typer.Typer(
    name="Vocabulary Builder",
    add_completion=False,
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
)


"""
APP COMMANDS
"""

@app.command()
def bye():
    """
    Say bye to the CLI
    """
    print(":wave: [bold green]Bye bye![/bold green]")


# todo @anay: write PyTest for this. Cover all cases/flags/arguments
@app.command(rich_help_panel="Dictionary", help="📚 [bold blue]Lookup[/bold blue] a word in the dictionary")
def define(
    word: str = typer.Argument(..., help="Word to search"),
    short: Optional[bool] = typer.Option(False, help="Lightweight definitions."),
    pronounce: Optional[bool] = typer.Option(False, help="Pronounce the word."),
    tag: Optional[str] = typer.Option(None, help="Tag the word in your vocabulary builder set.")
):
    """
    Shows the definition of WORD. 
    Adds it to the vocabulary builder list along with the timestamp if the user is logged in.
    """

    if short:
        Dictionary.definition(word, short=True)


    if not short:
        Dictionary.definition(word, short=False)
        
    
    if pronounce:
        Dictionary.pronounce(query=word)
        
    if tag:
        Dictionary.tag(word, tag)
    
    if not tag:
        Dictionary.tag(word)
    
    
    
# todo @anay: add a command to show word list [either all or by tag or by date or by learning/mastered]
# Make use of the following functions that you will be writing in Dictionary.py
# get_all_words()
# get_words_of_tag()
# get_words_from_learning_list()
# get_words_from_mastered_list()


    
if __name__ == "__main__":
    app()
