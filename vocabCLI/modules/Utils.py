import contextlib
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from sqlite3 import *
from typing import *

import requests
import typer
from Database import createConnection, createTables
from Dictionary import *
from Exceptions import *
from playsound import playsound
from requests import exceptions
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def check_word_exists(query: str) -> bool:
    """
    Checks if the word exists in the database

    Args:
        query (str): Word which is to be checked

    Raises:
        WordNeverSearchedException: If the word is not found in the database

    Returns:
        bool: True if word exists in the database
    """

    conn = createConnection()
    c = conn.cursor()
    # check if word exists in the database
    with contextlib.suppress(WordNeverSearchedException):
        c.execute("SELECT * FROM words WHERE word=?", (query,))
        if not c.fetchone():
            raise WordNeverSearchedException(query)
        return True


def fetch_word_history(word: str) -> None:
    """
    Fetches all instances of timestamp for a word from the database
    1. Execute a query that selects the datetime column from the words table where the word column is equal to the word
    2. If the word is not found in the database, raise an exception
    3. If the word is found in the database, print the history of the word

    Args:
        word (str): word for which history is to be fetched

    Raises:
        WordNeverSearchedException: If the word is not found in the database
    """

    conn = createConnection()
    c = conn.cursor()

    with contextlib.suppress(WordNeverSearchedException):
        c.execute(
            "SELECT datetime FROM words WHERE word=? ORDER by datetime DESC", (word,)
        )
        rows = c.fetchall()

        # ----------------- Table -----------------#

        table = Table(show_header=True, header_style="bold green")
        table.add_column("History", style="cyan")
        if len(rows) <= 0:
            raise WordNeverSearchedException(word)
        count = len(rows)
        print(
            Panel(
                f"You have searched for [bold]{word}[/bold] {count} time(s) before. 🔎"
            )
        )

        for row in rows:
            history = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime(
                "%d %b '%y | %H:%M"
            )
            table.add_row(history)
            table.add_section()
        print(table)

        # ----------------- Table -----------------#


def add_tag(query: str, tagName: str) -> None:
    """
    Tags the word in the vocabulary builder list.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database with no tags, then add the tag to add words
    4. If the word exists in the database with the same tag, then do nothing
    5. If the word exists in the database with a different tag, then overwrite the tag
    6. Print the success message

    Args:
        query (str): Word which is to be tagged.
        tagName (Optional[str], optional): Tag name which is to be added to the word and inserts it into the database. Defaults to None.

    Raises:
        WordNeverSearchedException: If the word is not found in the database
    """

    conn = createConnection()
    c = conn.cursor()
    # check if word exists in the database
    check_word_exists(query)

    # if word already exists in the database with no tags, then add the tag to add words
    c.execute("SELECT * FROM words WHERE word=? and tag is NULL", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET tag=? WHERE word=?", (tagName, query))
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been tagged as [bold green]{tagName}[/bold green]. ✅",
            )
        )
        return

    # if word already exists in the database with tags, then overwrite the tags
    c.execute("SELECT * FROM words WHERE word=? and tag is not NULL", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET tag=? WHERE word=?", (tagName, query))
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"The tag of [bold blue]{query}[/bold blue] has been changed to [bold green]{tagName}[/bold green]. ✅",
            )
        )
        return


def remove_tag(query: str) -> None:
    """Removes the tag from the word in the database
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database with no tags, then do nothing
    4. If the word exists in the database with tags, then remove the tag
    5. Print the success message

    Args:
        query (str): Word for which the tag is to be removed

    Raises:
        WordNeverSearchedException: If the word is not found in the database
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE word=?", (query,))
    if c.fetchone():
        c.execute("SELECT word FROM words WHERE word=? and tag is not NULL", (query,))
        if c.fetchone():
            # word exists with tag
            c.execute("UPDATE words SET tag=NULL WHERE word=?", (query,))
            conn.commit()
            print(
                Panel(
                    title="[b reverse green]  Tag Deleted!  [/b reverse green]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"Tags [bold red]deleted[/bold red] for the word [bold blue]{query}[/bold blue]. ✅",
                )
            )
        else:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"[bold blue]{query}[/bold blue] was not tagged. ❌",
                )
            )
    else:
        # word exits without tag
        raise WordNeverSearchedException(query)


def set_mastered(query: str) -> None:
    """
    Sets the word as mastered.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and mastered is set to 1, then do nothing
    4. If the word exists in the database and learning is set to 1, then set mastered to 1 and learning to 0
    5. If the word exists in the database and mastered is set to 0, then set it to 1
    6. Print the success message

    Args:
        query (str): Word which is to be set as mastered.

    Raises:
        WordNeverSearchedException: If the word is not found in the database
    """

    conn = createConnection()
    c = conn.cursor()

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
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been set as [bold green]mastered[/bold green]. Good work! ✅",
            )
        )


def check_mastered(query: str) -> bool:
    """
    Checks if the word is mastered and returns a boolean value.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and mastered is set to 1, then return True
    4. If the word exists in the database and mastered is set to 0, then return False

    Args:
        query (str): word which is to be checked for mastered status

    Returns:
        bool: True if the word is mastered, False otherwise
    """
    conn = createConnection()
    c = conn.cursor()

    c.execute("SELECT mastered FROM words WHERE word=? and mastered=1", (query,))
    return bool(row := c.fetchall())


def check_learning(query: str) -> bool:
    """
    Checks if the word is learning and returns a boolean value.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and learning is set to 1, then return True
    4. If the word exists in the database and learning is set to 0, then return False

    Args:
        query (str): word which is to be checked for learning status

    Returns:
        bool: True if the word is learning, False otherwise
    """
    conn = createConnection()
    c = conn.cursor()

    c.execute("SELECT learning FROM words WHERE word=? and learning=1", (query,))
    return bool(row := c.fetchall())


def set_unmastered(query: str) -> None:
    """
    Sets the word as unmastered.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and mastered is set to 0, then do nothing
    4. If the word exists in the database and mastered is set to 1, then set it as 0
    5. Print the success message

    Args:
        query (str): Word which is to be set as unmastered.
    """

    conn = createConnection()
    c = conn.cursor()

    # check if word exists in database
    check_word_exists(query)

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 0))
    if c.fetchone():
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] was never mastered. ❌",
            )
        )
        return

    c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been set as [bold red]unmastered[/bold red]. Remember to practice it. ✅",
            )
        )


def set_learning(query: str) -> None:
    """
    Sets the word as learning.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and is already learning, then do nothing
    4. If the word exists in the database and is mastered is set to 1, then set learning to 1 and mastered to 0
    5. If the word exists in the database and is mastered is set to 0, then set learning to 1
    6. Print the success message

    Args:
        query (str): Word which is to be set as learning.
    """

    conn = createConnection()
    c = conn.cursor()

    # warn user if word is never looked up before
    check_word_exists(query)

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=1", (query,))
    if c.fetchone():
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=f"🛑 [bold yellow]WARNING[/bold yellow] Are you sure you want to move word [bold blue]{query}[/bold blue] from [b]mastered to learning[/b]?",
            )
        )
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
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been set as [bold green]learning[/bold green]. Keep revising! 🧠",
            )
        )


def set_unlearning(query: str) -> None:
    """
    Sets the word as unlearning.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and learning is set to 0, then do nothing
    4. If the word exists in the database and learning is set to 1, then set it 0
    5. Print the success message

    Args:
        query (str): Word which is to be set as unlearning.
    """

    conn = createConnection()
    c = conn.cursor()

    # check if word exists in database
    check_word_exists(query)

    # check if word is not already unlearned
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 0))
    if c.fetchone():
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] was never learning. ❌",
            )
        )
        return

    # check if word is already learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        c.execute("UPDATE words SET learning=0 WHERE word=?", (query,))

    if c.rowcount > 0:
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been removed from [bold red]learning[/bold red]. ✅",
            )
        )


def set_favorite(query: str) -> None:
    """
    Sets the word as favorite.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and favorite is set to 1, then do nothing
    4. If the word exists in the database and favorite is set to 0, then set it to 1
    5. Print the success message

    Args:
        query (str): Word which is to be set as favorite.
    """

    conn = createConnection()
    c = conn.cursor()

    # warn user if word is never looked up before
    check_word_exists(query)

    # check if word is already favorite
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 1))
    if c.fetchone():
        print(
            Panel(
                f"[bold blue]{query}[/bold blue] is already marked as [bold green]favorite[/bold green]. 💙"
            )
        )
        return

    c.execute("UPDATE words SET favorite=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been set as [bold green]favorite[/bold green]. 💙",
            )
        )


def set_unfavorite(query: str) -> None:
    """
    Remove the word from favorite list.
    1. Check if the word exists in the database
    2. If the word does not exist in the database, raise an exception
    3. If the word exists in the database and favorite is set to 0, then do nothing
    4. If the word exists in the database and favorite is set to 1, then set it to 0
    5. Print the success message

    Args:
        query (str): Word which is to be removed from favorite.
    """

    conn = createConnection()
    c = conn.cursor()

    # check if word exists in database
    check_word_exists(query)

    # check if word was never favorited
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 0))
    if c.fetchone():
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] was never favorite. ❌",
            )
        )
        return

    # set word to favorite
    c.execute("UPDATE words SET favorite=0 WHERE word=?", (query,))

    if c.rowcount > 0:
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold blue]{query}[/bold blue] has been removed from [bold red]favorite[/bold red]. ✅",
            )
        )


# no tests for this function as it is not called anywhere in the command directly
def count_all_words() -> int:
    """
    Counts the distinct number of words in the database.

    Returns:
        int: Total word count.
    """

    conn = createConnection()
    c = conn.cursor()
    sql = "SELECT DISTINCT word FROM words"
    c.execute(sql)
    return len(rows) if (rows := c.fetchall()) else 0


# no tests for this function as it is not called anywhere in the command directly
def count_mastered() -> int:
    """
    Counts the distinct number of mastered words in the database.

    Returns:
        int: Total mastered word count.
    """

    conn = createConnection()
    c = conn.cursor()
    sql = "SELECT DISTINCT word FROM words WHERE mastered=1"
    c.execute(sql)
    return len(rows) if (rows := c.fetchall()) else 0


# no tests for this function as it is not called anywhere in the command directly
def count_learning() -> int:
    """
    Counts the distinct number of learning words in the database.

    Returns:
        int: Total learning word count.
    """

    conn = createConnection()
    c = conn.cursor()
    sql = "SELECT DISTINCT word FROM words WHERE learning=1"
    c.execute(sql)
    return len(rows) if (rows := c.fetchall()) else 0


# no tests for this function as it is not called anywhere in the command directly
def count_favorite() -> int:
    """
    Counts the distinct number of favorite words in the database.

    Returns:
        int: Total favorite word count.
    """

    conn = createConnection()
    c = conn.cursor()
    sql = "SELECT DISTINCT word FROM words WHERE favorite=1"
    c.execute(sql)
    return len(rows) if (rows := c.fetchall()) else 0


# no tests for this function as it is not called anywhere in the command directly
def count_tag(tag: str) -> int:
    """
    Counts the distinct number of words in the database with a particular tag.

    Returns:
        int: Total word count of specific tag.
    """

    conn = createConnection()
    c = conn.cursor()
    sql = "SELECT DISTINCT word FROM words WHERE tag=?"
    c.execute(sql, (tag,))
    return len(rows) if (rows := c.fetchall()) else 0


def get_random_word_definition_from_api() -> None:
    """Gets a random word from the text file and gets its definition from the API."""

    lines = open("modules/_random_words.txt").read().splitlines()
    random_word = random.choice(lines).strip()
    print(Panel(f"A Random Word for You: [bold green]{random_word}[/bold green]"))
    definition(random_word)


def get_random_word_from_learning_set() -> None:
    """
    Gets a random word from the learning list.

    Raises:
        NoWordsInLearningListException: If there are no words in the learning list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT word FROM words WHERE learning=1 ORDER BY RANDOM() LIMIT 1"
    )
    rows = c.fetchall()

    with contextlib.suppress(NoWordsInLearningListException):
        if len(rows) <= 0:
            raise NoWordsInLearningListException()
        print(
            Panel(
                f"A Random word from your [bold blue]learning[/bold blue] words list: [bold blue]{rows[0][0]}[/bold blue]"
            )
        )
        definition(rows[0][0])


def get_random_word_from_mastered_set() -> None:
    """
    Gets a random word with definition from the mastered words list.

    Raises:
        NoWordsInMasteredListException: If there are no words in the mastered list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT word FROM words WHERE mastered=1 ORDER BY RANDOM() LIMIT 1"
    )
    rows = c.fetchall()

    with contextlib.suppress(NoWordsInMasteredListException):
        if len(rows) <= 0:
            raise NoWordsInMasteredListException()

        print(
            Panel(
                f"A Random word from your [bold green]mastered[/bold green] words list: [bold green]{rows[0][0]}[/bold green]"
            )
        )
        definition(rows[0][0])


def get_random_word_from_favorite_set() -> None:
    """
    Gets a random word from the favorite list.

    Raises:
        NoWordsInFavoriteListException: If there are no words in the favorite list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT word FROM words WHERE favorite=1 ORDER BY RANDOM() LIMIT 1"
    )
    rows = c.fetchall()
    with contextlib.suppress(NoWordsInFavoriteListException):
        if len(rows) <= 0:
            raise NoWordsInFavoriteListException()
        print(
            Panel(f"A Random word from your [gold1]favorite[/gold1] list: {rows[0][0]}")
        )
        definition(rows[0][0])


def get_random_word_from_tag(tagName: str) -> None:
    """
    Gets a random word from the vocabulary builder list with a particular tag.
    1.

    Args:
        tag (Optional[str], optional): Tag from which the random word should be. Defaults to None.

    Raises:
        NoSuchTagException: If the tag does not exist.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT DISTINCT word FROM words WHERE tag=? ORDER BY RANDOM() LIMIT 1",
        (tagName,),
    )
    rows = c.fetchall()
    with contextlib.suppress(NoSuchTagException):
        if len(rows) <= 0:
            raise NoSuchTagException(tag=tagName)
        print(
            Panel(
                f"A Random word from your [bold blue]vocabulary builder[/bold blue] list with the tag {tagName}: [bold blue]{rows[0][0]}[/bold blue]"
            )
        )
        definition(rows[0][0])


def show_list(
    favorite: Optional[bool] = False,
    learning: Optional[bool] = False,
    mastered: Optional[bool] = False,
    tag: Optional[bool] = None,
    days: Optional[int] = None,
    date: Optional[str] = None,
    last: Optional[int] = None,
    most: Optional[int] = None,
    tagnames: Optional[bool] = False,
) -> None:
    # sourcery skip: low-code-quality
    """
    Gets all the words in the vocabulary builder list.
    1. The code give a list of mastered, learning, favorite, words with a particular tag, most recent words, words added in a particular date or words added in the last n number of days or most recent words based on the arguments passed
    2. Based on the arguments passed, the code executes the respective SQL command
    1. If no arguments are passed, it gets all the words in the vocabulary builder list
    4. If the SQL command returns no words, an error message is printed to the user
    5. If the SQL command returns words, the words are printed to the user in a table format

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

    conn = createConnection()
    c = conn.cursor()

    if mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1")
        success_message = "[bold green]Mastered[/bold green]"
        error_message = (
            "You have not [bold green]mastered[/bold green] any words yet. ❌"
        )

    elif learning:
        c.execute("SELECT DISTINCT word FROM words WHERE learning=1")
        success_message = "[bold blue]Learning[/bold blue]"
        error_message = "You have not added any words to the [bold blue]learning list[/bold blue] yet. ❌"

    elif favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1")
        success_message = "[bold gold1]Favorite[/bold gold1]"
        error_message = "You have not added any words to the [bold gold1]favorite[/bold gold1] list yet. ❌"

    elif days:
        if days < 1:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Enter a positive number ➕",
                )
            )
            return

        c.execute(
            f"SELECT DISTINCT word FROM words where datetime > datetime('now' , '-{days} days')"
        )
        date_today = datetime.datetime.now().strftime("%d/%m/%Y")
        date_before = datetime.datetime.now() - timedelta(days=int(days))
        success_message = f"Words added to the vocabulary builder list from [bold blue]{date_before.strftime('%d/%m/%Y')}[/bold blue] TO [bold blue]{date_today}[/bold blue]"
        error_message = "No records found within this date range ❌"

    elif date:

        # accept inputs from prompt
        day = typer.prompt("DD")
        month = typer.prompt("MM")
        year = typer.prompt("YYYY")

        if len(day) == 1:
            day = f"0{day}"

        if len(month) == 1:
            month = f"0{month}"

        # check if the inputs are integers
        try:
            check_if_int = int(day)
            check_if_int = int(month)
            check_if_int = int(year)

        except ValueError as e:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Date values have to be integers ❌",
                )
            )

        # check if the inputs are of the correct length
        if len(str(year)) != 4 and len(str(month)) != 2 and len(str(day)) != 2:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Incorrect date format ❌ Expected: [bold green]DD-MM-YYYY[/bold green]",
                )
            )
            return

        # check if days, months and years are fall in the correct range
        if int(month) not in range(1, 13) or int(day) not in range(1, 32):
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Date must fall within calendar range 📅 Expected: [bold green]DD-MM-YYYY[/bold green]",
                )
            )
            return

        # check if the date is not in the future
        date = f"{year}-{month}-{day}"
        checker = datetime.datetime.strptime(date, "%Y-%m-%d")
        if checker > datetime.datetime.now():
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="[red]Date cannot be in the future.[/red] ❌",
                )
            )
            return

        # fetch records if all checks pass
        datefmt = f"{date}%"
        c.execute("SELECT DISTINCT word FROM words where datetime LIKE ?", (datefmt,))
        success_message = f"Words added to the vocabulary builder list on [bold blue]{day}/{month}/{year}[/bold blue]"
        error_message = f"No records found for [bold blue]{date}[/bold blue] ❌"

    elif tag:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=?", (tag,))
        success_message = f"Words with tag [bold magenta]{tag}[/bold magenta]"
        error_message = f"Tag {tag} does not exist. ❌"

    elif last:
        if last < 1:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Enter a positive number ➕",
                )
            )
            return

        c.execute(
            "SELECT DISTINCT (word), datetime FROM words ORDER BY datetime DESC LIMIT ?",
            (last,),
        )
        error_message = "You haven't searched for any words yet. ❌"

        rows = c.fetchall()
        if len(rows) <= 0:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=error_message,
                )
            )
        else:

            # ----------------- Table -----------------#

            table = Table(show_header=True, header_style="bold bright_cyan")
            table.add_column("Word", style="cyan", width=15)
            table.add_column("Last searched on", style="light_green")
            print(Panel(f"Last [bold blue][{len(rows)}][/bold blue] words searched"))
            for row in rows:
                table.add_row(row[0], row[1])
                table.add_section()
            print(table)

            # ----------------- Table -----------------#

        return

    elif most:
        if most < 1:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Enter a positive number ➕",
                )
            )
            return

        c.execute(
            "SELECT word, COUNT(word) AS `word_count` FROM words GROUP BY word ORDER BY `word_count` DESC LIMIT ?",
            (most,),
        )
        success_message = "[bold blue]Top[/bold blue] most searched words"
        error_message = "You haven't searched for any words yet. ❌"

        rows = c.fetchall()
        if len(rows) <= 0:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=error_message,
                )
            )
        else:

            # ----------------- Table -----------------#

            table = Table(show_header=True, header_style="bold bright_cyan")
            table.add_column("Word", style="cyan", width=15)
            table.add_column("Times searched", style="light_green")
            print(Panel(f"{success_message} [bold blue][{len(rows)}][/bold blue]"))
            for row in rows:
                table.add_row(row[0], str(row[1]))
                table.add_section()
            print(table)

            # ----------------- Table -----------------#

        return

    elif tagnames:
        c.execute("SELECT DISTINCT tag FROM words WHERE tag is not NULL")
        success_message = "[bold magenta]YOUR TAGS :[/bold magenta]"
        error_message = "You haven't added any tags to your words yet. ❌"

    elif (
        favorite is False
        and learning is False
        and mastered is False
        and tag is None
        and date is None
        and last is None
        and most is None
        and tagnames is False
    ):
        c.execute("SELECT DISTINCT word FROM words")
        success_message = "Here is your list of words"
        error_message = "You have no words in your vocabulary builder list. ❌"

    rows = c.fetchall()
    if len(rows) <= 0:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=error_message,
            )
        )
    else:
        print(Panel(f"{success_message} [bold blue][{len(rows)} word(s)][/bold blue]"))
        rows = [Panel(f"[deep_pink4]{row[0]}[deep_pink4]", expand=True) for row in rows]

        # ----------------- Columns -----------------#

        print(Columns(rows, equal=True, expand=True))

        # ----------------- Columns -----------------#


def delete_all() -> None:
    """
    Deletes all the words from the database.

    Raises:
        NoWordsInDBException: If there are no words in the database.
    """

    conn = createConnection()
    c = conn.cursor()
    rowcount = count_all_words()

    with contextlib.suppress(NoWordsInDBException):
        if rowcount == 0:
            raise NoWordsInDBException()

        c.execute("DELETE FROM words")
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"All words [{c.rowcount}] [bold red]deleted[/bold red] from all your lists. ✅",
            )
        )


def delete_mastered() -> None:
    """
    Deletes all the mastered words from the database.

    Raises:
        NoWordsInMasteredListException: If there are no mastered words in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    rowcount = count_mastered()
    with contextlib.suppress(NoWordsInMasteredListException):
        if rowcount == 0:
            raise NoWordsInMasteredListException()

        c.execute("DELETE FROM words WHERE mastered=1")
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"All [bold green]mastered[/bold green] words [{rowcount}] [bold red]deleted[/bold red] from your lists. ✅",
            )
        )


def delete_learning() -> None:
    """
    Deletes all the learning words from the database.

    Raises:
        NoWordsInLearningListException: If there are no learning words in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    rowcount = count_learning()
    with contextlib.suppress(NoWordsInLearningListException):
        if rowcount == 0:
            raise NoWordsInLearningListException()

        c.execute("DELETE FROM words WHERE learning=1")
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"All [bold blue]learning[/bold blue] words [{rowcount}][bold red] deleted[/bold red] from your lists. ✅",
            )
        )


def delete_favorite() -> None:
    """
    Deletes all the favorite words from the database.

    Raises:
        NoWordsInFavoriteListException: If there are no favorite words in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    rowcount = count_favorite()
    with contextlib.suppress(NoWordsInFavoriteListException):
        if rowcount == 0:
            raise NoWordsInFavoriteListException()

        c.execute("DELETE FROM words WHERE favorite=1")
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"All [bold gold1]favorite[/bold gold1] words [{rowcount}][bold red] deleted[/bold red] from your lists. ✅",
            )
        )


def delete_words_from_tag(tag: str) -> None:
    """
    Deletes all the words from a particular tag from the database.

    Args:
        tag (str): The tag to delete words from.

    Raises:
        NoSuchTagException: If the tag doesn't exist in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    rowcount = count_tag(tag)
    with contextlib.suppress(NoSuchTagException):
        if rowcount == 0:
            raise NoSuchTagException(tag=tag)

    c.execute("DELETE FROM words WHERE tag=?", (tag,))
    conn.commit()
    print(
        Panel(
            title="[b reverse green]  Success!  [/b reverse green]",
            title_align="center",
            padding=(1, 1),
            renderable=f"All words [{rowcount}] with tag [bold magenta]{tag}[/bold magenta] [bold red]deleted[/bold red] from your lists. ✅",
        )
    )


def delete_word(query: List[str]) -> None:
    """
    Deletes a word from the database.

    Args:
        query (str): Word to be deleted.
    """

    conn = createConnection()
    c = conn.cursor()

    check_word_exists(query)

    sql = "DELETE FROM words WHERE word=?"
    c.execute(sql, (query,))
    if c.rowcount > 0:
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"Word [bold u]{query}[/bold u][bold red] deleted[/bold red] from your lists. ✅",
            )
        )


def clear_learning() -> None:
    """
    Clears all the words marked as learning.

    Raises:
        NoWordsInLearningListException: If there are no words in the learning list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("UPDATE words SET learning=0 WHERE learning=1")

    with contextlib.suppress(NoWordsInLearningListException):
        if c.rowcount <= 0:
            raise NoWordsInLearningListException()
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable="[bold green]All words[/bold green] have been removed from [bold red]learning[/bold red]. ✅",
            )
        )


def clear_mastered() -> None:
    """
    Clears all the words marked as mastered.

    Raises:
        NoWordsInMasteredListException: If there are no words in the mastered list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("UPDATE words SET mastered=0 WHERE mastered=1")

    with contextlib.suppress(NoWordsInMasteredListException):
        if c.rowcount <= 0:
            raise NoWordsInMasteredListException()
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable="[bold green]All words[/bold green] have been removed from [bold red]mastered[/bold red]. ✅",
            )
        )


def clear_favorite() -> None:
    """
    Clears all the words marked as favorite.

    Raises:
        NoWordsInFavoriteListException: If there are no words in the favorite list.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("UPDATE words SET favorite=0 WHERE favorite=1")

    with contextlib.suppress(NoWordsInFavoriteListException):
        if c.rowcount <= 0:
            raise NoWordsInFavoriteListException()
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Success!  [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable="[bold green]All words[/bold green] have been removed from [bold red]favorite[/bold red]. ✅",
            )
        )


def clear_all_words_from_tag(tagName: str) -> None:
    """
    Clears all the words with specific tag.

    Args:
        tagName (str): The tag to clear words from.

    Raises:
        NoSuchTagException: If the tag doesn't exist in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    c.execute("UPDATE words SET tag=NULL where tag=?", (tagName,))
    with contextlib.suppress(NoSuchTagException):
        if c.rowcount <= 0:
            raise NoSuchTagException(tag=tagName)
        conn.commit()
        print(
            Panel(
                title="[b reverse green]  Delete Successful! [/b reverse green]",
                title_align="center",
                padding=(1, 1),
                renderable=f"[bold green]All words[/bold green] have been removed from the tag {tagName}. ✅",
            )
        )


def get_lookup_rate(
    today: bool = False, week: bool = False, month: bool = False, year: bool = False
) -> None:
    """
    Returns the learning rate of the user.
    1. If today, then get the number of words learned today, yesterday and the difference between them
    2. If week, then get the number of words learned this week, last week and the difference between them
    3. If month, then get the number of words learned this month, last month and the difference between them
    4. If year, then get the number of words learned this year, last year and the difference between them
    5. If no option is given, then print an error message

    Args:
        today (bool, optional): If True, returns the lookup rate for today. Defaults to False.
        week (bool, optional): If True, returns the lookup rate for the week. Defaults to False.
        month (bool, optional): If True, returns the lookup rate for the month. Defaults to False.
        year (bool, optional): If True, returns the lookup rate for the year. Defaults to False.
    """

    conn = createConnection()
    c = conn.cursor()

    if today:
        # get today's learning words
        c.execute("SELECT COUNT(word) FROM words WHERE date(datetime)=date('now')")
        learning_count_today = c.fetchone()[0]

        # get yesterdays learning words
        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)=date('now', '-1 day')"
        )
        learning_count_yesterday = c.fetchone()[0]

        try:
            percentage = round(
                (learning_count_today - learning_count_yesterday)
                / (learning_count_yesterday)
                * 100,
                2,
            )
        except ZeroDivisionError:
            percentage = 100
        if percentage >= 0:
            print(
                Panel(
                    f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words today compared to yesterday.\n[violet]Today[/violet]: {learning_count_today} words.\n[violet]Yesterday[/violet]: {learning_count_yesterday} words.",
                    title="[reverse]Today's Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )
        else:
            print(
                Panel(
                    f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words today compared to yesterday.\n[violet]Today[/violet]: {learning_count_today} words.\n[violet]Yesterday[/violet]: {learning_count_yesterday} words.",
                    title="[reverse]Today's Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

    elif week:
        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-7 day')"
        )
        learning_count_week = c.fetchone()[0]

        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-14 day') AND date(datetime)<date('now', '-7 day')"
        )
        learning_count_last_week = c.fetchone()[0]

        try:
            percentage = round(
                (learning_count_last_week) / (learning_count_week) * 100, 2
            )
        except ZeroDivisionError:
            percentage = 100

        if percentage >= 0:
            print(
                Panel(
                    f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this week compared to last week.\n[violet]This week[/violet]: {learning_count_week} words.\n[violet]Last week[/violet]: {learning_count_last_week} words.",
                    title="[reverse]Weekly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

        else:
            print(
                Panel(
                    f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this week compared to last week.\n[violet]This week[/violet]: {learning_count_week} words.\n[violet]Last week[/violet]: {learning_count_last_week} words.",
                    title="[reverse]Weekly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

    elif month:
        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-1 month')"
        )
        learning_count_month = c.fetchone()[0]

        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-2 month') AND date(datetime)<date('now', '-1 month')"
        )
        learning_count_last_month = c.fetchone()[0]

        try:
            percentage = round(
                (learning_count_month - learning_count_last_month)
                / (learning_count_month)
                * 100,
                2,
            )
        except ZeroDivisionError:
            percentage = 100

        if percentage >= 0:
            print(
                Panel(
                    f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this month compared to last month.\n[violet]This month[/violet]: {learning_count_month} words.\n[violet]Last month[/violet]: {learning_count_last_month} words.",
                    title="[reverse]Monthly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

        else:
            print(
                Panel(
                    f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this month compared to last month.\n[violet]This month[/violet]: {learning_count_month} words.\n[violet]Last month[/violet]: {learning_count_last_month} words.",
                    title="[reverse]Monthly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

    elif year:
        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-1 year')"
        )
        learning_count_year = c.fetchone()[0]

        c.execute(
            "SELECT COUNT(word) FROM words WHERE date(datetime)>=date('now', '-2 year') AND date(datetime)<date('now', '-1 year')"
        )
        learning_count_last_year = c.fetchone()[0]

        try:
            percentage = round(
                (learning_count_year - learning_count_last_year)
                / (learning_count_year)
                * 100,
                2,
            )
        except ZeroDivisionError:
            percentage = 100

        if percentage >= 0:
            print(
                Panel(
                    f"🚀 You have looked up [bold green]{percentage}%[/bold green] [u]MORE[/u] words this year compared to last year.\n[violet]This year[/violet]: {learning_count_year} words.\n[violet]Last year[/violet]: {learning_count_last_year} words.",
                    title="[reverse]Yearly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

        else:
            print(
                Panel(
                    f"😓 You have looked up [bold red]{percentage}%[/bold red] [u]LESS[/u] words this year compared to last year.\n[violet]This year[/violet]: {learning_count_year} words.\n[violet]Last year[/violet]: {learning_count_last_year} words.",
                    title="[reverse]Yearly Learning Rate[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )

    else:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="[bold red] you cannot combine options with learning rate command[/bold red] ❌",
            )
        )


def get_consecutive_dates(dates: list) -> tuple:
    """
    Returns list of consecutive dates from list of dates
    1. Sort the list of dates
    2. Iterate through the list of dates
    3. If the difference between the current date and the next date is 1 day, continue
    4. If the difference between the current date and the next date is not 1 day, append the start date and the current date to the list of consecutive dates
    5. Set the start date to the next date
    6. Return the item with the longest time difference

    Args:
        dates (list): list of dates

    Returns:
        tuple: tuple of consecutive dates
    """

    consecutive_dates = []
    start_date = dates[0]

    for i in range(len(dates) - 1):
        if dates[i + 1] - dates[i] == datetime.timedelta(days=1):
            continue
        consecutive_dates.append((start_date, dates[i]))
        start_date = dates[i + 1]

    consecutive_dates.append((start_date, dates[-1]))

    # return the item with the longest time difference
    return max(consecutive_dates, key=lambda x: x[1] - x[0])


def show_streak() -> None:
    """
    Shows streak of days user has looked up words
    1. Check if there are any words in the database.
    2. If there are words, get all the dates from the database.
    3. Convert dates to datetime objects
    4. Sort dates
    5. Get consecutive dates
    6. Get difference between consecutive dates
    7. Print streak
    """

    conn = createConnection()
    c = conn.cursor()

    try:
        c.execute("SELECT DISTINCT(date(datetime)) FROM words")
        if not c.fetchone():
            raise NoWordsInDBException()

        c.execute("SELECT DISTINCT(date(datetime)) FROM words")
        dates = c.fetchall()

        # convert dates to datetime objects
        for i in range(len(dates)):
            dates[i] = datetime.datetime.strptime(dates[i][0], "%Y-%m-%d")

        # sort dates
        dates.sort()

        max_streak = get_consecutive_dates(dates)
        streak_days = max_streak[1] - max_streak[0]

        # convert streak_days to days
        streak_days = int(streak_days.days) + 1

        print(
            Panel(
                f"🔥 Your longest word lookup streak is [bold green]{streak_days}[/bold green] day(s).\n[violet]Start Date[/violet]: {max_streak[0].strftime('%d %B %Y')}\n[violet]End Date[/violet]: {max_streak[1].strftime('%d %B %Y')}",
                title="[reverse]Streak[/reverse]",
                title_align="center",
                padding=(1, 1),
            )
        )

    except NoWordsInDBException as e:
        print(e)


def predict_milestone(milestone: int) -> None:
    """
    Predicts when user will reach a milestone
    1. It runs a query to get the number of words in the database.
    2. If there are no words in the database, it throws an exception and prints a message.
    3. If there are words in the database, it runs a query to get the date of the most recent word looked up (last_date).
    4. It then runs a query to get the date of the first word looked up (first_date).
    5. It calculates the average words per day.
    6. It calculates the date of reaching the milestone (milestone_date).
    7. It prints the average words per day, the number of words learnt, and the date of reaching the milestone

    Parameters:
        milestone (int): milestone to predict
    """

    conn = createConnection()
    c = conn.cursor()

    c.execute("SELECT DISTINCT word FROM words")

    with contextlib.suppress(NoWordsInDBException):
        if not c.fetchone():
            print(
                Panel(
                    "Cannot predict milestone as you have not looked up any words yet."
                )
            )
            raise NoWordsInDBException()

        c.execute("SELECT COUNT(DISTINCT word) FROM words")

        learning_count = c.fetchone()[0]

        # if user has already reached milestone
        if milestone - learning_count <= 0:
            print(
                Panel(
                    f"👏🏻 You have already reached [bold green]{milestone}[/bold green] words.",
                    title="[reverse]Milestone Prediction[/reverse]",
                    title_align="center",
                    padding=(1, 1),
                )
            )
        else:
            # get the date of the most recent word looked up
            c.execute("SELECT date(datetime) FROM words ORDER BY datetime DESC LIMIT 1")
            last_date = datetime.datetime.strptime(c.fetchone()[0], "%Y-%m-%d")

            # get the date of the first word looked up
            c.execute("SELECT date(datetime) FROM words ORDER BY datetime ASC LIMIT 1")
            first_date = datetime.datetime.strptime(c.fetchone()[0], "%Y-%m-%d")

            # average words per day
            try:
                average_words_per_day = (
                    learning_count / (datetime.datetime.now() - first_date).days
                )
                average_words_per_day = round(average_words_per_day, 2)

                # calculate date to reach milestone based on average words per day
                milestone_date = datetime.datetime.now() + datetime.timedelta(
                    days=(milestone - learning_count) / average_words_per_day
                )

                # print average words per day
                print(
                    Panel(
                        f"You have been learning [bold green]{average_words_per_day}[/bold green] words on average per day. 🤔\n\nYou have learnt: {learning_count} words. Just {milestone-learning_count} more to go! 🚵🏻\n\nBased on your current word lookup rate, you will reach [bold green]{milestone}[/bold green] words on [bold green]{milestone_date.strftime('%d %B %Y')}[/bold green].",
                        title="[reverse]Milestone Prediction[/reverse]",
                        title_align="center",
                        padding=(1, 1),
                    )
                )
            except ZeroDivisionError:
                print(Panel("Keep learning words to get a prediction."))
