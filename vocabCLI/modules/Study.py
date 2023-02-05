import contextlib
import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import *

import questionary
import requests
import typer
from Database import createConnection, createTables
from Dictionary import *
from Exceptions import *
from questionary import Style
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Utils import *

#####################
# REVISE FUNCTIONS #
#####################


def start_revision(c: Cursor, is_collection: bool = False) -> None:
    """
    Starts the revision process.

    1. Fetches all the words in the collection from the database
    2. For each word in the collection, it prints out the word and its definition
    3. It asks the user if they want to set the word as learning
    4. If the user says yes, then the word is set as learning
    5. If the user says no, then the user is asked if they want to set the word as mastered
    6. If the user says yes, then the word is set as mastered
    7. If the user says no, then the user is asked if they want to stop revising
    8. If the user says yes, then the program stops revising, else it continues revising

    Args:
        c: cursor object
        is_collection: boolean to check if the revision is from a collection, default is False.
    """

    rows = c.fetchall()
    for count, row in enumerate(rows, start=1):
        print(
            Panel(
                title=f"[reverse]Revising word: [bold green]{count} / {len(rows)}[/bold green][/reverse]",
                title_align="center",
                renderable=f"{len(rows)-count} word(s) to go. Keep revising! 🧠",
            )
        )
        definition(row[0])
        if is_collection and not check_learning(row[0]):
            print(
                Panel(
                    f"Set [bold blue]{row[0]}[/bold blue] as [bold green]learning[/bold green] ?"
                )
            )
            if sure := typer.confirm(""):
                set_learning(row[0])
            else:
                print(
                    Panel(
                        f"OK, not setting [bold blue]{row[0]}[/bold blue] as learning, you can always revise it via our collection ✍🏼"
                    )
                )
                print("\n\n")

        # if word is not mastered then prompt user to set it as mastered
        elif not check_mastered(row[0]):
            print(
                Panel(
                    f"Set [bold blue]{row[0]}[/bold blue] as [bold green]mastered[/bold green] ?"
                )
            )
            if sure := typer.confirm(""):
                set_mastered(row[0])
            else:
                print(
                    Panel(
                        f"OK, not setting [bold blue]{row[0]}[/bold blue] as mastered, keep learning. ✍🏼"
                    )
                )
                print("\n\n")
        else:
            print(Panel("Press Y to Stop Revision. Enter to continue 📖"))
            if not (sure := typer.confirm("")):
                continue
            print(Panel("OK, stopping revision. 🛑"))
            break
    # else:
    #     print(Panel(title="[b reverse red]  Error!  [/b reverse red]",
    #             title_align="center",
    #             padding=(1, 1),
    #             renderable="No words to revise in the selected category. Look up some more words first by using 'define' command.")
    #     )


def revise_all(
    number: Optional[int] = None,
) -> None:  # sourcery skip: remove-redundant-if
    """
    Revise all words in the database.

    1. If number is not specified, then all words are revised.
    2. If number is specified, then only that many words are revised.
    3. If there are no words in the database, then an exception is raised.

    Args:
        number: number of words to revise, default is None.

    Raises:
        NoWordsInDBException: if there are no words in the database.
    """

    conn = createConnection()
    c = conn.cursor()

    # checks if there are any words in the database and breaks out if there are none
    with contextlib.suppress(NoWordsInDBException):
        if count_all_words() == 0:
            raise NoWordsInDBException()
    if not number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM()")
        start_revision(c)

    elif number:
        c.execute(
            "SELECT DISTINCT word FROM words ORDER BY RANDOM() LIMIT ?", (number,)
        )
        start_revision(c)


def revise_tag(
    number: Optional[int] = None, tag: Optional[str] = None
) -> None:  # sourcery skip: remove-redundant-if
    """
    Revise words in a specific tag.

    Args:
        number: number of words to revise, default is None.
        tag: tag to revise, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if tag is not found
    if tag:
        with contextlib.suppress(NoSuchTagException):
            if count_tag(tag) == 0:
                raise NoSuchTagException(tag=tag)
    if tag and not number:
        c.execute(
            "SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM()", (tag,)
        )
        start_revision(c)

    elif number and tag:
        c.execute(
            "SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM() LIMIT ?",
            (tag, number),
        )
        start_revision(c)


def revise_learning(
    number: Optional[int] = None,
) -> None:
    """
    Revise words in learning list.

    Args:
        number: number of words to revise, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if no words learning
    with contextlib.suppress(NoWordsInLearningListException):
        if count_learning() == 0:
            raise NoWordsInLearningListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM()")
        start_revision(c)

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_revision(c)


def revise_mastered(
    number: Optional[int] = None,
) -> None:
    """
    Revise words in mastered list.

    Args:
        number: number of words to revise, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if no words learning

    with contextlib.suppress(NoWordsInMasteredListException):
        if count_mastered() == 0:
            raise NoWordsInMasteredListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM()")
        start_revision(c)

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_revision(c)


def revise_favorite(
    number: Optional[int] = None,
) -> None:
    """
    Revise words in favorite list.

    Args:
        number: number of words to revise, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    with contextlib.suppress(NoWordsInFavoriteListException):
        if count_favorite() == 0:
            raise NoWordsInFavoriteListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_revision(c)

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_revision(c)


def revise_collection(
    number: Optional[int] = None, collectionName: Optional[str] = None
) -> None:
    """
    Revise words in a collection.

    Args:
        number: number of words to revise, default is None.
        collectionName: name of the collection, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    if collectionName:
        with contextlib.suppress(NoSuchCollectionException):
            c.execute(
                "SELECT word FROM collections where collection=?", (collectionName,)
            )
            if not c.fetchone():
                raise NoSuchCollectionException(collection=collectionName)

    if collectionName and not number:
        c.execute(
            "SELECT word FROM collections where collection=? ORDER BY RANDOM()",
            (collectionName,),
        )
        start_revision(c, is_collection=True)

    elif number and collectionName:
        c.execute(
            "SELECT word FROM collections where collection=? ORDER BY RANDOM() LIMIT ?",
            (collectionName, number),
        )
        start_revision(c, is_collection=True)


#####################
# QUIZ FUNCTIONS #
#####################


def start_quiz(
    c: Cursor, collection=None, quizType: str = None
) -> None:  # sourcery skip: remove-redundant-if
    """
    Starts the quiz.

    1. Fetches all the words in the collection or in the database, depending on the quiz type.
    2. Breaks out if the collection has less than 4 words, as the minimum number of words in a quiz is 4.
    3. Sets the style of the quiz.
    4. Initializes the score and timer.
    5. Iterates over the words in the collection/database.
    6. Sets up the question.
    7. Fetches the correct answer for the question.
    8. Sets up the list of choices. If the quiz type is collection, the list of choices is made up of the correct answer and three fake answers from the collection. Otherwise, the list of choices is made up of the correct answer and three fake answers from the database.
    9. Asks the question to the user and checks if the answer is correct.
    10. If the answer is correct, increases the score and prints the success message. Otherwise, prints the failure message.
    11. Prints the quiz summary and inserts the quiz history into the database.

    Args:
        c: cursor object.
        type: type of the quiz. Must be one of "all words", "learning words", "mastered words", "favorite words", "collection: collectionName", "tag:tagName".
        collection: name of the collection, default is None.
    """

    if not (rows := c.fetchall()):
        return

    # break out if -n < 4
    with contextlib.suppress(NotEnoughWordsForQuizException):
        if len(rows) < 4:
            raise NotEnoughWordsForQuizException()

        # setting quiz style
        fancy_style = Style(
            [
                ("qmark", "fg:#673ab7 bold"),
                ("question", "fg:#0000ff bold"),
                ("answer", "fg:#ffff00 bold"),
                ("pointer", "fg:#ffd700 bold"),
                ("highlighted", "fg:#0000ff bold"),
                ("selected", "fg:#cc5454"),
                ("separator", "fg:#cc5454"),
                ("instruction", "fg:#673ab7 bold"),
            ]
        )

        # initializing score and timer
        score = 0
        tic = datetime.now()

        # iterating over questions
        for count, row in enumerate(rows, start=1):

            # setting up question
            quiz_word = row[0]

            print(
                Panel(
                    title=f"[reverse]Question [bold green]#{count}/{len(rows)}[/bold green][/reverse]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"Choose the correct definition for: [bold u blue]{quiz_word}[/bold u blue]",
                )
            )

            # answer
            correct_definition = one_line_definition(quiz_word)

            # question list with the correct answer
            choices = [correct_definition]

            # if taking quiz on a collection then only fake choices from the collection otherwise the answer will be obvious
            if collection:
                c.execute(
                    "SELECT DISTINCT word FROM collections where collection=? and word!=? ORDER BY RANDOM() LIMIT 3",
                    (
                        collection,
                        quiz_word,
                    ),
                )

            # adding 3 fake choices from words in the database.
            else:
                c.execute(
                    "SELECT DISTINCT word FROM words where word!=? ORDER BY RANDOM() LIMIT 3",
                    (quiz_word,),
                )
            choices.extend(one_line_definition(row[0]) for row in c.fetchall())
            random.shuffle(choices)

            user_choice = questionary.select(
                f"",
                choices=choices,
                style=fancy_style,
                show_selected=True,
                use_arrow_keys=True,
                use_indicator=True,
                qmark="",
                instruction=" ",
            ).ask()

            if user_choice == correct_definition:
                score += 1
                print(Panel(f"✅ Correct! Score: [bold green]{score}[/bold green]"))
            else:
                print(
                    Panel(
                        f"❌ Incorrect! Score: [bold green]{score}[/bold green]\nCorrect answer was: [bold green]{correct_definition}[/bold green]"
                    )
                )
            print("\n\n")

        toc = datetime.now()
        diff = toc - tic

        seconds = diff.seconds
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(
            Panel(
                title="[b reverse white]  Quiz completed!  [/b reverse white]",
                title_align="center",
                padding=(1, 1),
                renderable=f"🎯 [bold bright_magenta u]Score[/bold bright_magenta u]: [bold green]{score}[/bold green] / [bold green]{len(rows)}[/bold green]\n⏰ [bold bright_magenta u]Time Elapsed[/bold bright_magenta u]: [blue]{minutes:0.0f}M {seconds:0.0f}S[/blue]",
            )
        )

        # inserting quiz history into the database
        c.execute(
            "INSERT INTO quiz_history (type, datetime, question_count,points,duration) values (?, ?, ?, ?, ?)",
            (
                quizType,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(rows),
                score,
                diff.seconds,
            ),
        )
        c.close()


def quiz_all(
    number: Optional[int] = None,
) -> None:  # sourcery skip: remove-redundant-if
    """
    Quiz all words in the database.

    Args:
        number: number of words to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # checks if there are any words in the database and breaks out if there are none
    with contextlib.suppress(NoWordsInDBException):
        if count_all_words() == 0:
            raise NoWordsInDBException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM()")
        start_quiz(c, quizType="all words")
        conn.commit()

    elif number:
        c.execute(
            "SELECT DISTINCT word FROM words ORDER BY RANDOM() LIMIT ?", (number,)
        )
        start_quiz(c, quizType="all words")
        conn.commit()


def quiz_tag(
    number: Optional[int] = None, tag: Optional[str] = None
) -> None:  # sourcery skip: remove-redundant-if
    """
    Quiz words with a specific tag.

    Args:
        number: number of words to quiz, default is None.
        tag: tag to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if tag is not found
    if tag:
        with contextlib.suppress(NoSuchTagException):
            if count_tag(tag) == 0:
                raise NoSuchTagException(tag=tag)

    if tag and not number:
        c.execute(
            "SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM()", (tag,)
        )
        start_quiz(c, quizType=f"tag: {tag}")
        conn.commit()

    elif number and tag:
        c.execute(
            "SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM() LIMIT ?",
            (tag, number),
        )
        start_quiz(c, quizType=f"tag: {tag}")
        conn.commit()


def quiz_learning(number: Optional[int] = None) -> None:
    """
    Quiz words in learning list.

    Args:
        number: number of words to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if no words learning

    with contextlib.suppress(NoWordsInLearningListException):
        if count_learning() == 0:
            raise NoWordsInLearningListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM()")
        start_quiz(c, quizType="learning words")
        conn.commit()

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_quiz(c, quizType="learning words")
        conn.commit()


def quiz_mastered(number: Optional[int] = None) -> None:
    """
    Quiz words in mastered list.

    Args:
        number: number of words to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if no words learning
    with contextlib.suppress(NoWordsInMasteredListException):
        if count_mastered() == 0:
            raise NoWordsInMasteredListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM()")
        start_quiz(c, quizType="mastered words")
        conn.commit()

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_quiz(c, quizType="mastered words")
        conn.commit()


def quiz_favorite(number: Optional[int] = None) -> None:
    """
    Quiz words in favorite list.

    Args:
        number: number of words to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    # will stop the execution if no words learning
    with contextlib.suppress(NoWordsInFavoriteListException):
        if count_favorite() == 0:
            raise NoWordsInFavoriteListException()

    if not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_quiz(c, quizType="favorite words")
        conn.commit()

    if number:
        c.execute(
            "SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?",
            (number,),
        )
        start_quiz(c, quizType="favorite words")
        conn.commit()


# TODO: - quiz will break and throw an error if words in the collection are not available in the api definition. Also, quiz_collection will be generally slow because it has to fetch the definition for each word in the option, find a way to make it fast.
def quiz_collection(
    number: Optional[int] = None, collectionName: Optional[str] = None
) -> None:
    """
    Quiz words in a collection.

    Args:
        number: number of words to quiz, default is None.
        collectionName: name of collection to quiz, default is None.
    """

    conn = createConnection()
    c = conn.cursor()

    if collectionName:
        with contextlib.suppress(NoSuchCollectionException):
            c.execute(
                "SELECT word FROM collections where collection=?", (collectionName,)
            )
            if not c.fetchone():
                raise NoSuchCollectionException(collection=collectionName)

    if collectionName and not number:
        c.execute(
            "SELECT word FROM collections where collection=? ORDER BY RANDOM()",
            (collectionName,),
        )
        start_quiz(
            c, collection=collectionName, quizType=f"collection: {collectionName}"
        )
        conn.commit()

    elif number and collectionName:
        c.execute(
            "SELECT word FROM collections where collection=? ORDER BY RANDOM() LIMIT ?",
            (collectionName, number),
        )
        if c.fetchone() is None:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"Collection '{collectionName}' is empty",
                )
            )
            return
        start_quiz(
            c, collection=collectionName, quizType=f"collection: {collectionName}"
        )
        conn.commit()


def show_quiz_history() -> None:
    """
    Show quiz history.

    1. Execute SQL SELECT statement to get all the rows from the quiz_history table.
    2. If there are no rows, print a message and return.
    3. Else print the quiz history in a table.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_history ORDER BY datetime DESC")
    rows = c.fetchall()
    if not rows:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="No quiz attempts yet. Take a quiz to see your quiz history.",
            )
        )
        return

    # ----------------- Table -----------------#

    table = Table(show_header=True, header_style="bold green")
    table.add_column("Quiz Type", style="cyan")
    table.add_column("Date & Time of Attempt")
    table.add_column("Score")
    table.add_column("Duration")

    for row in rows:
        history = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S").strftime(
            "%d %b '%y | %H:%M"
        )
        score = f"{row[3]}/{row[2]}"
        duration = f"{row[4]} seconds"
        table.add_row(row[0], history, score, duration)
        table.add_section()
    print(table)

    # ----------------- Table -----------------#
