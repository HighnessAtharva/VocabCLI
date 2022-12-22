import calendar
import json
import sqlite3
import threading
import requests
from datetime import datetime
from sqlite3 import Error
from requests import exceptions
from rich import print
from rich.panel import Panel
# from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress import track

#no tests for this function as it is not called anywhere in the command directly
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


#no tests for this function as it is not called anywhere in the command directly
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

    collections="""CREATE TABLE IF NOT EXISTS "collections" (
            "word"	TEXT NOT NULL,
            "collection" TEXT NOT NULL
            );
        """

    try:
        c = conn.cursor()
        c.execute(words)
        c.execute(cache_words)
        c.execute(collections)

    except Exception as e:
        print(e)


#no tests for this function as it is not called anywhere in the command directly
def initializeDB():
    """ Initializes the database """

    conn=createConnection()
    createTables(conn)



# NOTE: Use this command very sparingly. It is not recommended to use this command more than once a week due to possible API overuse
def refresh_cache():
    """
    Refreshes the cache of the words in the database.
    """
    
    # check if cache is empty, if yes then do nothing
    conn=createConnection()
    c=conn.cursor()

    c.execute("SELECT COUNT(*) FROM cache_words")
    if not c.fetchone()[0]:
        return
    c.execute("SELECT word FROM cache_words")
    rows=c.fetchall()

    total=0
    for row in rows:
        #----------------- Progress Bar -----------------#
        for _ in track(range(len(rows)), description=" 🔃 Refreshing Cache "):
            
        #----------------- Progress Bar -----------------#

            
                word=row[0]
                try:
                    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
                    response.raise_for_status()

                except exceptions.ConnectionError as error:
                    print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                        title_align="center",
                        padding=(1, 1),
                        renderable="[bold red]Error: You are not connected to the internet.[/bold red] ❌")
                )
                else:
                    if response.status_code == 200:
                        c.execute("UPDATE cache_words SET api_response=? WHERE word=?", (json.dumps(response.json()[0]), word))
                        conn.commit()
                    
                # update the progress bar
                total += 1
                
    print(Panel.fit(title="[b reverse green]  Success!  [/b reverse green]", 
                     title_align="center",
                     padding=(1, 1),
                     renderable="Cache refreshed successfully.")
        ) 