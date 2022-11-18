import typer
from typing import *
from rich import print
import Dictionary
from Database import *
from DictionaryUtils import *


# initialize the database with the tables if not already existing
initializeDB()

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
    
    
    

 
    
if __name__ == "__main__":
    app()
