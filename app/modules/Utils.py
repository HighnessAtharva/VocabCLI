import contextlib
import json
import os
import random
import typer
import requests
from Database import createConnection, createTables
from Dictionary import *
from Exceptions import *
from datetime import datetime
from datetime import timedelta 
from pathlib import Path
from sqlite3 import *
from typing import *
from playsound import playsound
from requests import exceptions
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


#no tests for this function as it is not called anywhere in the command directly
def check_word_exists(query: str):
    """
    Checks if the word exists in the database

    Args:
        query (str): Word which is to be checked
    """

    conn= createConnection()
    c=conn.cursor()
    # check if word exists in the database
    with contextlib.suppress(WordNeverSearchedException):
        c.execute("SELECT * FROM words WHERE word=?", (query,))
        if not c.fetchone():
            raise WordNeverSearchedException(query)
        return True


def fetch_word_history(word: str):  # sourcery skip: extract-method
    """
    Fetches all instances of timestamp for a word from the database

    Args:
        word (str): word for which history is to be fetched
    """

    conn=createConnection()
    c=conn.cursor()

    try:
        c.execute("SELECT datetime FROM words WHERE word=? ORDER by datetime DESC", (word,))
        rows=c.fetchall()
        table=Table(show_header=True, header_style="bold green")
        table.add_column("History", style="cyan")
        if len(rows) <= 0:
            raise WordNeverSearchedException(word)
        count=len(rows)
        print(Panel(f"You have searched for [bold]{word}[/bold] {count} time(s) before. 🔎"))
        
        for row in rows:
            history=datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%d %b\' | %y %H:%M')
            table.add_row(history)
            table.add_section()
        print(table)
    except WordNeverSearchedException as e:
        pass


def add_tag(query: str, tagName:str):
    """
    Tags the word in the vocabulary builder list.

    Args:
        query (str): Word which is to be tagged.
        tagName (Optional[str], optional): Tag name which is to be added to the word and inserts it into the database. Defaults to None.
    """

    conn=createConnection()
    c=conn.cursor()
    # check if word exists in the database
    check_word_exists(query)

    # if word already exists in the database with no tags, then add the tag to add words
    c.execute("SELECT * FROM words WHERE word=? and tag is NULL", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET tag=? WHERE word=?", (tagName, query))
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been tagged as [bold green]{tagName}[/bold green]. ✅"))
        return

    # if word already exists in the database with tags, then overwrite the tags
    c.execute("SELECT * FROM words WHERE word=? and tag is not NULL", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET tag=? WHERE word=?", (tagName, query))
        conn.commit()
        print(Panel(f"The tag of [bold blue]{query}[/bold blue] has been changed to [bold green]{tagName}[/bold green]. ✅"))
        return

def remove_tag(query: str):
    """Removes the tag from the word in the database

    Args:
        query (str): Word for which the tag is to be removed
    """

    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT * FROM words WHERE word=?", (query,))
    if c.fetchone():
        c.execute("SELECT word FROM words WHERE word=? and tag is not NULL", (query,))
        if c.fetchone():
            # word exists with tag
            c.execute("UPDATE words SET tag=NULL WHERE word=?", (query,))
            conn.commit()
            print(Panel(f"Tags deleted for the word [bold blue]{query}[/bold blue]. ✅"))
        else:
            print(Panel(f"[bold blue]{query}[/bold blue] was not tagged. ❌"))
    else:
        # word exits without tag
        raise WordNeverSearchedException(query)




# word doesn't exist
def set_mastered(query: str):
    """
    Sets the word as mastered.

    Args:
        query (str): Word which is to be set as mastered.
    """

    conn=createConnection()
    c=conn.cursor()

    # warn user if word is never looked up before
    check_word_exists(query)

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 1))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] is already marked as mastered. ✅"))
        return


    # check if word is set to learning and remove it from learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        c.execute("UPDATE words SET learning=0 WHERE word=?", (query,))


    c.execute("UPDATE words SET mastered=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been set as [bold green]mastered[/bold green]. Good work! ✅"))



def set_unmastered(query: str):
    """
    Sets the word as unmastered.

    Args:
        query (str): Word which is to be set as unmastered.
    """

    conn=createConnection()
    c=conn.cursor()

    #check if word exists in database
    check_word_exists(query)

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 0))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] was never mastered. ❌"))
        return

    c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been set as [bold red]unmastered[/bold red]. Remember to practice it."))



def set_learning(query: str):
    """
    Sets the word as learning.

    Args:
        query (str): Word which is to be set as learning.
    """

    conn=createConnection()
    c=conn.cursor()

    # warn user if word is never looked up before
    check_word_exists(query)

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=1", (query,))
    if c.fetchone():
        print(Panel(f"🛑 [bold yellow]WARNING[/bold yellow] Are you sure you want to move word [bold blue]{query}[/bold blue] from [b]mastered to learning[/b]?"))
        if sure := typer.confirm(""):
            c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
        else:
            print(Panel(f"OK, not moving [bold blue]{query}[/bold blue] to learning."))
            return

    # check if word is already learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] is already marked as learning. ✅"))
        return

    # set word as learning
    c.execute("UPDATE words SET learning=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been set as [bold green]learning[/bold green]. Keep revising! 🧠"))



def set_unlearning(query: str):
    """
    Sets the word as unlearning.

    Args:
        query (str): Word which is to be set as unlearning.
    """

    conn=createConnection()
    c=conn.cursor()

    #check if word exists in database
    check_word_exists(query)

    # check if word is not already unlearned
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 0))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] was never learning. ❌"))
        return

    # check if word is already learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        c.execute("UPDATE words SET learning=0 WHERE word=?", (query,))

    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been removed from [bold red]learning[/bold red].")    )




def set_favorite(query: str):
    """
    Sets the word as favorite.

    Args:
        query (str): Word which is to be set as favorite.
    """

    conn=createConnection()
    c=conn.cursor()

    # warn user if word is never looked up before
    check_word_exists(query)

    # check if word is already favorite
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 1))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] is already marked as [bold green]favorite[/bold green]. 💙"))
        return

    c.execute("UPDATE words SET favorite=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been set as [bold green]favorite[/bold green]. 💙"))



def set_unfavorite(query:str):
    """
    Remove the word from favorite list.

    Args:
        query (str): Word which is to be removed from favorite.
    """

    conn=createConnection()
    c=conn.cursor()

    #check if word exists in database
    check_word_exists(query)

    # check if word was never favorited
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 0))
    if c.fetchone():
        print(Panel(f"[bold blue]{query}[/bold blue] was never favorite. ❌"))
        return

    # set word to favorite
    c.execute("UPDATE words SET favorite=0 WHERE word=?", (query,))

    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold blue]{query}[/bold blue] has been removed from [bold red]favorite[/bold red]. ✅"))


#no tests for this function as it is not called anywhere in the command directly
def count_all_words() -> int:
    """
    Counts the distinct number of words in the database.

    Returns:
        int: Total word count.
    """

    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words"
    c.execute(sql)
    if rows := c.fetchall():
        return len(rows)
    print(Panel("There are no words in the database. 🤷"))
    return 0


#no tests for this function as it is not called anywhere in the command directly
def count_mastered() -> int:
    """
    Counts the distinct number of mastered words in the database.

    Returns:
        int: Total mastered word count.
    """

    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE mastered=1"
    c.execute(sql)
    if rows := c.fetchall():
        return len(rows)
    print(Panel("There are no mastered words. 🤷"))
    return 0


#no tests for this function as it is not called anywhere in the command directly
def count_learning() -> int:
    """
    Counts the distinct number of learning words in the database.

    Returns:
        int: Total learning word count.
    """

    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE learning=1"
    c.execute(sql)
    if rows := c.fetchall():
        return len(rows)
    print(Panel("[bold red]No words are learning. 🤷[/bold red]"))
    return 0


#no tests for this function as it is not called anywhere in the command directly
def count_favorite() -> int:
    """
    Counts the distinct number of favorite words in the database.

    Returns:
        int: Total favorite word count.
    """

    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE favorite=1"
    c.execute(sql)
    if rows := c.fetchall():
        return len(rows)
    print(Panel("[bold red]There are no favorite words. 🤷[/bold red]"))
    return 0


#no tests for this function as it is not called anywhere in the command directly
def count_tag(tag:str) -> int:
    """
    Counts the distinct number of words in the database with a particular tag.

    Returns:
        int: Total word count of specific tag.
    """

    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE tag=?"
    c.execute(sql, (tag,))
    if rows := c.fetchall():
        return len(rows)
    print(Panel(f"[bold red]Tag {tag} does not exist. 🤷[/bold red]"))
    return 0


def get_random_word_definition_from_api():
    """
    Gets a random word from the text file and gets its definition from the API.
    """
    lines = open('modules/files/most_common_words.txt').read().splitlines()
    random_word =random.choice(lines).strip()
    print(Panel(f"A Random Word for You: [bold green]{random_word}[/bold green]"))
    definition(random_word)



def get_random_word_from_learning_set():
    """
    Gets a random word from the learning list.

    """

    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT word FROM words WHERE learning=1 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel("You have no words in your vocabulary builder learning list. 👀"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [bold blue]learning[/bold blue] words list: [bold blue]{row[0]}[/bold blue]"))
            definition(row[0])


def get_random_word_from_mastered_set():
    """
    Gets a random word with definition from the mastered words list.

    Args:
        tag (Optional[str], optional): Tag from which the mastered word should be. Defaults to None.
    """

    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT word FROM words WHERE mastered=1 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel("You have not mastered any words yet. 👀"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [bold green]mastered[/bold green] words list: [bold green]{row[0]}[/bold green]"))
            definition(row[0])

def get_random_word_from_favorite_set():
    """ Gets a random word from the favorite list."""
    
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT word FROM words WHERE favorite=1 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel("You have no favorite words. 👀"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [gold1]favorite[/gold1] list: {row[0]}"))

def get_random_word_from_tag(tagName:str):
    """
    Gets a random word from the vocabulary builder list with a particular tag.

    Args:
        tag (Optional[str], optional): Tag from which the random word should be. Defaults to None.
    """

    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT word FROM words WHERE tag=? ORDER BY RANDOM() LIMIT 1", (tagName,))
    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel(f"No words in your list with the tag {tagName}. ❌"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [bold blue]vocabulary builder[/bold blue] list with the tag {tagName}: [bold blue]{row[0]}[/bold blue]"))
            definition(row[0])

# FIXME @atharva: debug only tag argument 🐞
def show_list(
    favorite:Optional[bool]=False,
    learning:Optional[bool]=False,
    mastered:Optional[bool]=False,
    tag:Optional[bool]=None,
    days:Optional[int]=None,
    date:Optional[str]=None,
    last:Optional[int]=None,
    most: Optional[int]=None,
    tagnames:Optional[bool]=False
    ):
    # sourcery skip: low-code-quality
    """
    Gets all the words in the vocabulary builder list.
    Args:
        favorite (bool, optional): If True, gets list of favorite words. Defaults to False.
        learning (bool, optional): If True, gets list of learning words. Defaults to False.
        mastered (bool, optional): If True, gets list of mastered words. Defaults to False.
        tag (string, optional): Gets the list of words of the mentioned tag. Defaults to None.
        days (int, optional): Get a list of words from last n number of days. Defaults to None.
        date (string, optional): Get a list of words from a particular date. Defaults to None.
        last (string, optional):"Get a list of n last searched words. Defaults to None.
        most (string, optional): Get a list of n most searched words. Defaults to None.
        tagnames (bool, optional): If True, gets list of all tags. Defaults to False.
    """

    conn=createConnection()
    c=conn.cursor()

    if mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1")
        success_message = "[bold green]Mastered[/bold green]"
        error_message="You have not [bold green]mastered[/bold green] any words yet. ❌"

    elif learning:
        c.execute("SELECT DISTINCT word FROM words WHERE learning=1")
        success_message="[bold blue]Learning[/bold blue]"
        error_message="You have not added any words to the [bold blue]learning list[/bold blue] yet. ❌"

    elif favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1")
        success_message="[bold gold1]Favorite[/bold gold1]"
        error_message="You have not added any words to the [bold gold1]favorite[/bold gold1] list yet. ❌"

    elif days:
        if days<1:
            print(Panel("Enter a positive number ➕"))
            return

        c.execute(f"SELECT DISTINCT word FROM words where datetime > datetime('now' , '-{days} days')")
        date_today=datetime.datetime.now().strftime("%d/%m/%Y")
        date_before=datetime.datetime.now() - timedelta(days=int(days))
        success_message=f"Words added to the vocabulary builder list from [bold blue]{date_before.strftime('%d/%m/%Y')}[/bold blue] TO [bold blue]{date_today}[/bold blue]"
        error_message="No records found within this date range ❌"


    elif date:

        # accept inputs from prompt
        day=typer.prompt("DD")
        month=typer.prompt("MM")
        year=typer.prompt("YYYY")

        if len(day)==1:
            day = f"0{day}"

        if len(month)==1:
            month = f"0{month}"


        # check if the inputs are integers
        try:
            check_if_int=int(day)
            check_if_int=int(month)
            check_if_int=int(year)

        except ValueError as e:
            print(Panel("Date values have to be integers ❌")) 

        # check if the inputs are of the correct length
        if len(str(year))!=4 and len(str(month))!=2 and len(str(day))!=2:
            print(Panel("Incorrect date format ❌ Expected: [bold green]DD-MM-YYYY[/bold green]"))
            return

        # check if days, months and years are fall in the correct range
        if int(month) not in range(1,13) or int(day) not in range(1,32):
            print(Panel("Date must fall within calendar range 📅 Expected: [bold green]DD-MM-YYYY[/bold green]"))
            return

        # check if the date is not in the future
        date=f"{year}-{month}-{day}"
        checker=datetime.datetime.strptime(date, '%Y-%m-%d')
        if checker > datetime.datetime.now():
            print(Panel("[red]Date cannot be in the future.[/red] ❌"))
            return

        # fetch records if all checks pass
        datefmt=f"{date}%"
        c.execute("SELECT DISTINCT word FROM words where datetime LIKE ?", (datefmt,))
        success_message=f"Words added to the vocabulary builder list on [bold blue]{day}/{month}/{year}[/bold blue]"
        error_message=f"No records found for [bold blue]{date}[/bold blue] ❌"


    elif tag:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=?", (tag,))
        success_message=f"Words with tag [bold magenta]{tag}[/bold magenta]"
        error_message=f"Tag {tag} does not exist. ❌"

    elif last:
        if last<1:
            print(Panel("Enter a positive number ➕"))
            return

        c.execute("SELECT DISTINCT (word), datetime FROM words ORDER BY datetime DESC LIMIT ?", (last,))
        error_message="You haven't searched for any words yet. ❌"

        rows=c.fetchall()
        if len(rows) <= 0:
            print(Panel(error_message))
        else:
            table=Table(show_header=True, header_style="bold bright_cyan")
            table.add_column("Word", style="cyan", width=15)
            table.add_column("Last searched on", style="light_green")
            print(Panel(f"Last [bold blue][{len(rows)}][/bold blue] words searched"))
            for row in rows:
                table.add_row(row[0], row[1])
                table.add_section()
            print(table)
        return

    elif most:
        if most<1:
            print(Panel("Enter a positive number ➕"))
            return

        c.execute("SELECT word, COUNT(word) AS `word_count` FROM words GROUP BY word ORDER BY `word_count` DESC LIMIT ?", (most,))
        success_message="[bold blue]Top[/bold blue] most searched words"
        error_message="You haven't searched for any words yet. ❌"

        rows=c.fetchall()
        if len(rows) <= 0:
            print(Panel(error_message))
        else:
            table=Table(show_header=True, header_style="bold bright_cyan")
            table.add_column("Word", style="cyan", width=15)
            table.add_column("Times searched", style="light_green")
            print(Panel(f"{success_message} [bold blue][{len(rows)}][/bold blue]"))
            for row in rows:
                table.add_row(row[0], str(row[1]))
                table.add_section()
            print(table)
        return

    elif tagnames:
        c.execute("SELECT DISTINCT tag FROM words WHERE tag is not NULL")
        success_message = "[bold magenta]YOUR TAGS :[/bold magenta]"
        error_message="You haven't added any tags to your words yet. ❌"

    elif favorite is False and learning is False and mastered is False and tag is None and date is None and last is None and most is None and tagnames is False:
        c.execute("SELECT DISTINCT word FROM words")
        success_message="Here is your list of words"
        error_message="You have no words in your vocabulary builder list. ❌"

    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel(error_message))
    else:
        print(Panel(f"{success_message} [bold blue][{len(rows)} word(s)][/bold blue]"))
        rows = [Panel(f"[deep_pink4]{row[0]}[deep_pink4]", expand=True) for row in rows]
        print(Columns(rows, equal=True))

 
def delete_all():
    """ Deletes all the words from the database. """

    conn=createConnection()
    c=conn.cursor()
    rowcount=count_all_words()
    if rowcount==0:
        print(Panel("[bold red]Nothing to delete.[/bold red] Look up some words first. 🔎"))
        return

    c.execute("DELETE FROM words")
    conn.commit()
    print(Panel(f"All words [{rowcount}] [bold red]deleted[/bold red] from all your lists. ✅"))


def delete_mastered():
    """ Deletes all the mastered words from the database. """

    conn=createConnection()
    c=conn.cursor()

    rowcount=count_mastered()
    if rowcount==0:
        print(Panel("[bold red]No words in your mastered list.[/bold red] Add some first. ➕"))
        return

    c.execute("DELETE FROM words WHERE mastered=1")
    conn.commit()
    print(Panel(f"All [bold green]mastered[/bold green] words [{rowcount}] [bold red]deleted[/bold red] from your lists. ✅"))


def delete_learning():
    """Deletes all the learning words from the database."""

    conn=createConnection()
    c=conn.cursor()

    rowcount=count_learning()
    if rowcount==0:
        print(Panel("[bold red]No words in your learning list.[/bold red] Add some first. ➕"))
        return

    c.execute("DELETE FROM words WHERE learning=1")
    conn.commit()
    print(Panel(f"All [bold blue]learning[/bold blue] words [{rowcount}][bold red] deleted[/bold red] from your lists. ✅"))


def delete_favorite():
    """Deletes all the favorite words from the database."""

    conn=createConnection()
    c=conn.cursor()

    rowcount=count_favorite()
    if rowcount==0:
        print(Panel("[bold red]No words in your favorite list.[/bold red] Add some first. ➕"))
        return

    c.execute("DELETE FROM words WHERE favorite=1")
    conn.commit()
    print(Panel(f"All [bold gold1]favorite[/bold gold1] words [{rowcount}][bold red] deleted[/bold red] from your lists. ✅"))


def delete_words_from_tag(tag: str):
    """
    Deletes all the words from a particular tag from the database.

    Args:
        tag (str): The tag to delete words from.
    """

    conn=createConnection()
    c=conn.cursor()

    rowcount=count_tag(tag)
    if rowcount==0:
        print(Panel(f"[bold red]No words in tag {tag}.[/bold red] Add some first. ➕"))
        return

    c.execute("DELETE FROM words WHERE tag=?", (tag,))
    conn.commit()
    print(Panel(f"All words [{rowcount}] with tag [bold magenta]{tag}[/bold magenta] [bold red]deleted[/bold red] from your lists. ✅"))


def delete_word(query:List[str]):
    """
    Deletes a word from the database.

    Args:
        query (str): Word to be deleted.
    """

    conn=createConnection()
    c=conn.cursor()

    check_word_exists(query)

    sql="DELETE FROM words WHERE word=?"
    c.execute(sql, (query,))
    if c.rowcount>0:
        conn.commit()
        print(Panel(f"[bold red]Word {query} deleted[/bold red] from your lists. ✅"))


def clear_learning():
    """
    Clears all the words marked as learning.
    """

    conn=createConnection()
    c=conn.cursor()

    c.execute("UPDATE words SET learning=0 WHERE learning=1")
    if c.rowcount > 0:
        conn.commit()
        print(Panel("[bold green]All words[/bold green] have been removed from [bold red]learning[/bold red]. ✅"))
    else:
        print(Panel("[bold red]No words[/bold red] are marked as [bold red]learning[/bold red]. ❌"))


def clear_mastered():
    """
    Clears all the words marked as mastered.
    """

    conn=createConnection()
    c=conn.cursor()

    c.execute("UPDATE words SET mastered=0 WHERE mastered=1")
    if c.rowcount > 0:
        conn.commit()
        print(Panel("[bold green]All words[/bold green] have been removed from [bold red]mastered[/bold red]. ✅"))
    else:
        print(Panel("[bold red]No words[/bold red] are marked as [bold red]mastered[/bold red]. ❌"))


def clear_favorite():
    """
    Clears all the words marked as favorite.
    """

    conn=createConnection()
    c=conn.cursor()

    c.execute("UPDATE words SET favorite=0 WHERE favorite=1")
    if c.rowcount > 0:
        conn.commit()
        print(Panel("[bold green]All words[/bold green] have been removed from [bold red]favorite[/bold red]. ✅"))
    else:
        print(Panel("[bold red]No words[/bold red] are marked as [bold red]favorite[/bold red]. ❌"))


def clear_all_words_from_tag(tagName:str):
    """
    Clears all the words with specific tag.

    Args:
        tagName (str): The tag to clear words from.
    """

    conn=createConnection()
    c=conn.cursor()

    c.execute("UPDATE words SET tag=NULL where tag=?", (tagName,))
    if c.rowcount > 0:
        conn.commit()
        print(Panel(f"[bold green]All words[/bold green] have been removed from the tag {tagName}. ✅"))
    else:
        print(Panel(f"[bold red]No words[/bold red] with the tag {tagName} were found. ❌"))


def get_lookup_rate(today=False, week=False, month=False, year=False):
    """
    Returns the learning rate of the user.

    Args:
        today (bool, optional): If True, returns the lookup rate for today. Defaults to False.
        week (bool, optional): If True, returns the lookup rate for the week. Defaults to False.
        month (bool, optional): If True, returns the lookup rate for the month. Defaults to False.
        year (bool, optional): If True, returns the lookup rate for the year. Defaults to False.
    """

    conn=createConnection()
    c=conn.cursor()

    # todo fix formula
    if today:
        # get today's learning words
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)=date('now')")
        learning_count_today=c.fetchone()[0]

        # get yesterdays learning words
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)=date('now', '-1 day')")
        learning_count_yesterday=c.fetchone()[0]
        
        try:
            percentage=round((learning_count_today-learning_count_yesterday)/(learning_count_yesterday)*100, 2)
        except ZeroDivisionError:
            percentage=learning_count_today*100
        if percentage>=0:
            print(Panel(f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words today compared to yesterday.\n[violet]Today[/violet]: {learning_count_today} words.\n[violet]Yesterday[/violet]: {learning_count_yesterday} words.", title="[reverse]Today's Learning Rate[/reverse]", title_align="center"))
        else:
            print(Panel(f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words today compared to yesterday.\n[violet]Today[/violet]: {learning_count_today} words.\n[violet]Yesterday[/violet]: {learning_count_yesterday} words.", title="[reverse]Today's Learning Rate[/reverse]", title_align="center"))

    elif week:
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-7 day')")
        learning_count_week=c.fetchone()[0]

        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-14 day') AND date(datetime)<date('now', '-7 day')")
        learning_count_last_week=c.fetchone()[0]

        percentage=round((learning_count_last_week)/(learning_count_week)*100, 2)
        if percentage>=0:
            print(Panel(f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this week compared to last week.\n[violet]This week[/violet]: {learning_count_week} words.\n[violet]Last week[/violet]: {learning_count_last_week} words.", title="[reverse]Weekly Learning Rate[/reverse]", title_align="center"))

        else:
            print(Panel(f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this week compared to last week.\n[violet]This week[/violet]: {learning_count_week} words.\n[violet]Last week[/violet]: {learning_count_last_week} words.", title="[reverse]Weekly Learning Rate[/reverse]", title_align="center"))

    elif month:
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-1 month')")
        learning_count_month=c.fetchone()[0]

        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-2 month') AND date(datetime)<date('now', '-1 month')")
        learning_count_last_month=c.fetchone()[0]

        percentage=round((learning_count_month-learning_count_last_month)/(learning_count_month)*100, 2)
        if percentage>=0:
            print(Panel(f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this month compared to last month.\n[violet]This month[/violet]: {learning_count_month} words.\n[violet]Last month[/violet]: {learning_count_last_month} words.",title="[reverse]Monthly Learning Rate[/reverse]", title_align="center"))

        else:
            print(Panel(f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this month compared to last month.\n[violet]This month[/violet]: {learning_count_month} words.\n[violet]Last month[/violet]: {learning_count_last_month} words.",title="[reverse]Monthly Learning Rate[/reverse]", title_align="center"))

    elif year:
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-1 year')")
        learning_count_year=c.fetchone()[0]

        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-2 year') AND date(datetime)<date('now', '-1 year')")
        learning_count_last_year=c.fetchone()[0]

        percentage=round((learning_count_year-learning_count_last_year)/(learning_count_year)*100, 2)
        if percentage>=0:
            print(Panel(f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this year compared to last year.\n[violet]This year[/violet]: {learning_count_year} words.\n[violet]Last year[/violet]: {learning_count_last_year} words.",title="[reverse]Yearly Learning Rate[/reverse]", title_align="center"))

        else:
            print(Panel(f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this year compared to last year.\n[violet]This year[/violet]: {learning_count_year} words.\n[violet]Last year[/violet]: {learning_count_last_year} words.", title="[reverse]Yearly Learning Rate[/reverse]", title_align="center"))

    else:
        print(Panel("[bold red] you cannot combine options with learning rate command[/bold red] ❌"))
