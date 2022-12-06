import sqlite3
from sqlite3 import Error
from datetime import datetime
from rich import print
import calendar
import threading
import requests
from requests import exceptions
import json

def createConnection():
    """
    Creates a database connection to a SQLite database VocabularyBuilder.db

    Returns:
        Connection object or None.
    """
    conn = None
    try:
        conn = sqlite3.connect('./VocabularyBuilder.db')
    except Error as e:
        print(e)
    return conn


def createTables(conn: sqlite3.Connection):
    """
    Creates tables in the database

    Args:
        conn (sqlite3.Connection): Connection object
    """

    words="""CREATE TABLE IF NOT EXISTS "words" (
	"word"	TEXT,
	"datetime"	timestamp NOT NULL UNIQUE,
	"tag"	TEXT,
	"mastered"	INTEGER NOT NULL DEFAULT 0,
	"learning"	INTEGER NOT NULL DEFAULT 0,
	"favorite"	INTEGER NOT NULL DEFAULT 0
);
    """

    cache_words="""CREATE TABLE IF NOT EXISTS "cache_words" (
	"word"	TEXT NOT NULL UNIQUE,
    "api_response" json NOT NULL
);
    """

    try:
        c = conn.cursor()
        c.execute(words)
        c.execute(cache_words)

    except SQLException as e:
        print(e)


def initializeDB():
    """ Initializes the database """

    conn=createConnection()
    createTables(conn)



# todo - complete this function. Make a command for this. Do not add this function in PyTest or IP may be blocked due to constant requests
# NOTE: Use this command very sparingly. It is not recommended to use this command more than once a week due to possible API overuse
def refresh_cache():
    # check if cache is empty, if yes then do nothing
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM cache_words")
    if not c.fetchone()[0]:
        return

    print("Refreshing cache...")
    c.execute("SELECT word FROM cache_words")
    rows=c.fetchall()
    for row in rows:
        word=row[0]
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            response.raise_for_status()

        except exceptions.ConnectionError as error:
            print(Panel("[bold red]Error: You are not connected to the internet.[/bold red] ❌"))

        else:
            if response.status_code == 200:
                c.execute("UPDATE cache_words SET api_response=? WHERE word=?", (json.dumps(response.json()[0]), word))
                conn.commit()
    print("Cache refreshed successfully.")
