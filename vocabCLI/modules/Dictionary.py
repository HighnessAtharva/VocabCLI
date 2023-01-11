import os
import json
import requests
import time
import csv
from .Database import createConnection
from .Exceptions import *
from playsound import playsound
from pathlib import Path
from requests import exceptions
from datetime import datetime
from rich import print
from typing import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn



def display_theme(query: str)->None:
    conn=createConnection()
    c=conn.cursor()
    # join collection and words table to get the collection name for the word
    c.execute("SELECT collection FROM collections JOIN words ON collections.word=words.word WHERE words.word=?", (query,))
    if collection := c.fetchone():
        print(Panel(f"[bold cyan]Theme:[/bold cyan] {collection[0]}"))
  

def show_commonly_confused(word:str)->None:
    """Check if the word is commonly confused with other words, if yes, show them"""
    
    with open("modules/commonly_confused.csv", "r") as file:
        reader=csv.reader(file)
        for row in reader:
            if word in row:
                confused_list = [i for i in row if i!=word]                
                print(Panel(f"❕ [bold green]{word}[/bold green] is commonly confused with [bold green]{', '.join(confused_list)}[/bold green].", title="[reverse]Commonly Confused[/reverse]", title_align="center",padding=(1, 1)))    
                
                      
#no tests for this function as it is not called anywhere in the command directly
def connect_to_api(query:str="hello")->json:
    """
    Connects to the API and returns the response in JSON format.

    Args:
        query (str, optional): Word to lookup to test the API. Defaults to "hello".

    Returns:
        dict: Response in JSON format.
    """
    
    try:

        # sql query to check if word exists in the cache_word table
        conn=createConnection()
        c=conn.cursor()
        c.execute("SELECT * FROM cache_words WHERE word=?", (query,))

        # if word exists in the cache_word table, return the response from the cache_word table
        if c.fetchone():
            c.execute("SELECT api_response FROM cache_words WHERE word=?", (query,))
            return json.loads(c.fetchone()[0])

        # if word does not exist in the cache_word table, then connect to the API
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()

    except exceptions.ConnectionError as error:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]Error: You are not connected to the internet.[/bold red] ❌")
        ) 

    except exceptions.HTTPError as error:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"The word [bold red]{query}[/bold red] is not a valid word. Please check the spelling. ❌")
        )

    except exceptions.Timeout as error:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]Error: Timeout[/bold red] ⏳")
        )

    else:
        if response.status_code == 200:
            # insert the word and its response into the cache_word table if it isn't already there
            c.execute("SELECT * FROM cache_words WHERE word=?", (query,))
            if not c.fetchone():
                c.execute("INSERT INTO cache_words (word, api_response) VALUES (?, ?)", (query, json.dumps(response.json()[0])))
                conn.commit()

            # return the response from the API
            return response.json()[0]


#no tests for this function as it is not called anywhere in the command directly
def phonetic(query: str)-> str:
    """
    Prints the phonetic of the word.

    Args:
        query (str): Word for which phonetic is to be printed.

    Returns:
        string: Phonetic of the word.
    """

    if not (response := connect_to_api(query)):
        return
    if len(response["phonetics"])==0:
        phonetic="[bold red]Phonetic Unavailable[/bold red]"
    else:
        for phonetics in response["phonetics"]:
            if "text" in phonetics and len(phonetics["text"])>0:
                phonetic= phonetics["text"]
            else:
                phonetic= "[bold red]Phonetic Unavailable[/bold red] ❌"
    return(phonetic)


#no tests for this function as it is not called anywhere in the command directly
def insert_word_to_db(query: str)->None:
    """
    Tags the word in the vocabulary builder list.

    Args:
        query (str): Word which is to be tagged.
    """

    # check if word definitions exists. If yes, add to database otherwise do not do anything. Don't even print anything.
    try:
        # sql query to check if word exists in the cache_word table
        conn=createConnection()
        c=conn.cursor()
        c.execute("SELECT * FROM cache_words WHERE word=?", (query,))

        # if word exists in the cache_word table, return the response from the cache_word table
        if c.fetchone():
            conn=createConnection()
            time.sleep(1)
            insert_to_db_util(conn, query)
            return
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()

    except exceptions.HTTPError as error:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"The word [bold red]{query}[/bold red] is not a valid word. Please check the spelling. ❌")
        )
        return

    else:
        if response.status_code == 200:
            conn=createConnection()
            insert_to_db_util(conn, query)

#no tests for this function as it is not called anywhere in the command directly
def insert_to_db_util(conn, query: str)->None:
    """
    Inserts the word into the database.

    Args:
        conn (sqlite3.Connection): Connection to the database.
        query (str): Word to be inserted into the database.
    """

    c=conn.cursor()

    c.execute("SELECT * FROM words WHERE word=? and tag is not NULL", (query,))
    # if word is already tagged previously, insert it with the same tag
    if c.fetchone():
        c.execute("SELECT tag FROM words WHERE word=?", (query,))
        tagName=c.fetchone()[0]
        c.execute("INSERT INTO words (word, datetime, tag) VALUES (?, ?, ?)", (query, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), tagName))
    # if word is not tagged, insert it with no tag
    else:
        c.execute("INSERT INTO words (word, datetime) VALUES (?, ?)", (query, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()


    # if word already exists in the database with favorite 1, then update the above inserted record with favorite 1
    c.execute("SELECT favorite FROM words WHERE word=? and favorite=1", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET favorite=1 WHERE word=?", (query,))
        conn.commit()


    # if word already exists in the database with learning 1, then update the above inserted record with learning 1
    c.execute("SELECT learning FROM words WHERE word=? and learning=1", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET learning=1 WHERE word=?", (query,))
        conn.commit()


    # if word already exists in the database with mastered 1, then update the above inserted record with mastered
    c.execute("SELECT mastered FROM words WHERE word=? and mastered=1", (query,))
    if c.fetchone():
        c.execute("UPDATE words SET mastered=1 WHERE word=?", (query,))
        conn.commit()


def definition(query:str, short:Optional[bool]=False) -> None:
    """
    Prints the definition of the word.

    Args:
        query (str): Word which is meant to be defined.
        short (Optional[bool], optional): If True, it will print just the short definition. Defaults to False.
    """
    query=query.lower()
    #----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="moon", style="bold violet"),
        TextColumn("[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Searching...", total=None)
    #----------------- Spinner -----------------#
        
        if not (response := connect_to_api(query)):
            return

        # print(response)
        print(Panel(f"[bold gold1]{query.upper()}[/bold gold1]\n{phonetic(query)}"))

        table=Table(show_header=True, header_style="bold bright_cyan")
        table.add_column("Part of Speech", style="cyan", width=15)
        table.add_column("Definition", style="light_green")

        # insert search word into DB
        insert_word_to_db(query)

        if short:
            for meaningNumber in response["meanings"]:
                for meaning in meaningNumber["definitions"][:1]:
                    table.add_row(meaningNumber["partOfSpeech"], meaning["definition"])
                table.add_section()
            print(table)


        if not short:            
            # shows the associated collection for the word
            display_theme(query)
            show_commonly_confused(query)
            
            for meaningNumber in response["meanings"]:
                for count, meaning in enumerate(meaningNumber["definitions"], start=1):

                    # if example available
                    if "example" in meaning:
                        table.add_row(f"\n{meaningNumber['partOfSpeech']}", f"\n{count}. {meaning['definition']}\n[bold white u]Example:[/bold white u] [i white]{meaning['example']}[/i white]\n")

                    # if example not available
                    else:
                        table.add_row(f"\n{meaningNumber['partOfSpeech']}", f"\n{count}. {meaning['definition']}\n")
                table.add_section()
            print(table)
            print("\n")


#no tests for this function as it is not called anywhere in the command directly
def one_line_definition(query:str) -> str:
    """
    Prints the one line definition of the word.

    Args:
        query (str): Word which is meant to be defined.
    """

    if not (response := connect_to_api(query)):
        return

    for meaningNumber in response["meanings"]:
        for meaning in meaningNumber["definitions"][:1]:
            return (meaning["definition"])



#no tests for this function as it is not called anywhere in the command directly
def say_aloud(query: str) -> None:
    """
    Pronounces the word. Downloads the audio file, plays it and deletes it.

    Args:
        query (str): Word to be pronounced.

    """
    
    if not (response := connect_to_api(query)):
        return

    try:
        if len(response["phonetics"])==0:
            raise AudioUnavailableException

        phonetic = response["phonetics"][0] if "phonetics" in response else "phonetics not available"
        audioURL=phonetic["audio"] if "audio" in phonetic else None

        if audioURL in [None, ""]:
            raise AudioUnavailableException

        audio = requests.get(audioURL, allow_redirects=True)
        open(f'{query}.mp3', 'wb').write(audio.content)
        playsound(os.path.join(Path().cwd(), f"{query}.mp3"))
        print(Panel("[bold green]Audio played[/bold green] 🎧"))
        os.remove(f"{query}.mp3") if os.path.exists(f"{query}.mp3") else None

    except AudioUnavailableException as e:
        print(e)


# TODO: add a main command and link it to this function
def get_word_of_the_day() -> None:
    """Get a word of the day from a public API and print its definition."""

    WORDNIK_API_KEY = os.getenv("WORDNIK_API_KEY")
    response = requests.get(f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={WORDNIK_API_KEY}").json()    
    word = response["word"]
    print(Panel("[bold green]WORD OF THE DAY[/bold green] 📅"))
    
    definition(query=word, short=True)