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
# by default export all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: export words of a particular tag
# -l, --learning: export words from the learning list
# -m, --mastered: export words from the mastered list
# -f, --favorite: export words from the favorite list
# -d, --date DATE: export words from a particular date
# --most INT: export the most searched words (INT is the number of words to display)


# Make use of the following functions that you will be writing in Dictionary.py
# get_all_words()
# get_words_of_tag()
# get_words_from_learning_list()
# get_words_from_mastered_list()

    
    
# todo @anay: add export command to export the word list
# by default export all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: export words of a particular tag
# -l, --learning: export words from the learning list
# -m, --mastered: export words from the mastered list
# -f, --favorite: export words from the favorite list
# -d, --date DATE: export words from a particular date
# -to-csv (default): export to csv file
# -to-PDF: export to PDF file


# todo @anay: add a command to import the word list
# by default import all words in a csv file
# OPTIONS/FLAGS will be (two or more can be used at once):
# -t, --tag TAGNAME: import words of a particular tag
# -l, --learning: import words from the learning list
# -m, --mastered: import words from the mastered list
# -f, --favorite: import words from the favorite list
# -d, --date DATE: import words from a particular date


# todo @anay: add a command to set word as favorite


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


# todo @atharva: add a command to delete a word 
# OPTIONS/FLAGS will be (two or more can be used at once):
# DEFAULT: delete a specified word from the database
# -t, --tag: delete all words of a particular tag
# -l, --learning: delete all words from the learning list
# -m, --mastered: delete all words from the mastered list
# -f, --favorite: delete all words from the favorite list





if __name__ == "__main__":
    app()
