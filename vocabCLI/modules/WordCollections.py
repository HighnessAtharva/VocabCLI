import contextlib
import csv
import os

import pandas as pd
from Database import *
from Exceptions import *
from rich import box, print
from rich.columns import Columns
from rich.table import Table


def delete_collection_from_DB():
    """Deletes all rows from the collections table"""
    conn = createConnection()
    c = conn.cursor()
    c.execute("DELETE FROM collections")
    conn.commit()


def clean_collection_csv_data():
    """Cleans the domains.csv file and writes the cleaned data to domains.csv"""

    df = pd.read_csv("modules/domains.csv", encoding="latin-1")  # Read the CSV Files
    df["word"] = df["word"].str.lower()  # convert all words to lowercase
    # Remove the rows with spaces in the word column
    df = df[df["word"].str.contains(" ") == False]
    # Remove the rows with hyphen in the word column
    df = df[df["word"].str.contains("-") == False]
    # Remove the rows with apostrophe in the word column
    df = df[df["word"].str.contains("'") == False]
    # Remove the rows with quotes in the word column
    df = df[df["word"].str.contains('"') == False]
    # drop rows where word column and topic column have same value
    df = df.drop(df[(df["word"] == df["topic"])].index)
    df = df.drop_duplicates(subset="word")  # Remove duplicate rows
    # sort the dataframe by topic and word
    df = df.sort_values(by=["topic", "word"])
    df.reset_index(drop=True, inplace=True)  # reset index

    # delete words if length is less than 3
    for i in range(len(df)):
        if len(df["word"][i]) <= 2:
            df.drop(i, inplace=True)

    # delete the current domains.csv file
    os.remove("modules/domains.csv")

    # write to new csv
    df.to_csv("modules/domains.csv", index=False)

    # print(df.shape) # print row and column count
    # print(df.groupby('topic').count().sort_values(['word'],ascending=False)) # show word count grouped by topic and sorted by word count


def insert_collection_to_DB():
    """Inserts the cleaned data from domains.csv to the collections table in the database if the table is empty"""

    conn = createConnection()
    c = conn.cursor()

    # do not run if collection table already has data
    c.execute("SELECT * from collections")
    if c.fetchone():
        return

    clean_collection_csv_data()
    with open(file="modules/domains.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            word = row[0]
            collection_name = row[1]
            c.execute(
                "INSERT INTO collections (word, collection) VALUES (?, ?)",
                (word, collection_name),
            )
    conn.commit()


# todo @anay - formatting can be improved, add color, styles and emojis
def show_all_collections():
    """Shows all the collections in the database"""

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT count(word), collection FROM collections GROUP BY collection ORDER BY count(word) DESC"
    )
    rows = c.fetchall()

    # ----------------- Table -----------------#

    table = Table(title="Collections")
    table.add_column(
        "Words in Collection", justify="center", style="cyan", no_wrap=True
    )
    table.add_column("Collection Name", justify="center", style="cyan", no_wrap=True)
    for row in rows:
        table.add_row(str(row[0]), row[1])
    print(table)

    # ----------------- Table -----------------#


# todo @anay - formatting can be improved, add color, styles and emojis
def show_words_from_collection(collectionName: str):
    """Shows all the words in a collection

    Args:
        collectionName (str): Name of the collection

    Raises:
        NoSuchCollectionException: If the collection does not exist
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT word FROM collections WHERE collection=?", (collectionName,))
    rows = c.fetchall()
    with contextlib.suppress(NoSuchCollectionException):
        if len(rows) <= 0:
            raise NoSuchCollectionException(collection=collectionName)

        print(
            Panel(
                f"📚 Words from the collection {collectionName} [bold blue][{len(rows)} word(s)][/bold blue]"
            )
        )
        rows = [
            Panel(
                f"[b gold1 dim]{idx}[/b gold1 dim]. [dark_slate_gray1 i]{row[0]}[/dark_slate_gray1 i]",
                expand=True,
                box=box.SQUARE,
            )
            for idx, row in enumerate(rows, start=1)
        ]

        # ----------------- Columns -----------------#

        print(Columns(rows, expand=True))

        # ----------------- Columns -----------------#


# todo @anay - formatting can be improved, add color, styles and emojis
def get_random_word_from_collection(collectionName: str):
    """Shows a random word from a collection

    Args:
        collectionName (str): Name of the collection

    Raises:
        NoSuchCollectionException: If the collection does not exist
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT word FROM collections WHERE collection=? ORDER BY RANDOM() LIMIT 1",
        (collectionName,),
    )
    row = c.fetchone()
    with contextlib.suppress(NoSuchCollectionException):
        if row is None:
            raise NoSuchCollectionException(collection=collectionName)
        else:
            print(
                Panel(
                    title="[reverse blue]Random Word[/reverse blue]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"A random word from the [u green]{collectionName}[/u green] collection: [bold blue]{row[0]}[/bold blue]",
                )
            )
