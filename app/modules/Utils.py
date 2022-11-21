import os
import json
import requests
from playsound import playsound
from pathlib import Path
from requests import exceptions
from typing import *
from datetime import datetime
from rich import print
from rich.panel import Panel
from random_word import RandomWords
from Database import createConnection, createTables
from rich.console import Console
from rich.table import Table
from Dictionary import connect_to_api, definition


# todo @anay: add proper docstrings   ✅
def fetch_word_history(word):
    """ Fetches all instances of timestamp for a word from the database 

    Args:
        word (str): word for which history is to be fetched
    """
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT datetime FROM words WHERE word=? ORDER by datetime DESC", (word,))
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have not searched for this word before.")
    else:
        count=len(rows)
        print(f"You have searched for [bold]{word}[/bold] {count} times before.")
        for row in rows:
            history=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y %H:%M:%S')
            print(history)
            



# todo @anay: add proper docstrings     ✅
# todo @atharva: do not add the word to the database if the word defintion is unavailable in Dictionary  
def add_tag(query: str, tagName:Optional[str]=None):
    """
    Tags the word in the vocabulary builder list.

    Args:
        query (str): Word which is to be tagged.
        tagName (Optional[str], optional): Tag name which is to be added to the word. Defaults to None.
    """
     
    # check if word definitions exists. If yes, add to database otherwise do not do anything. Don't even print anything.    
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()
            
    except exceptions.HTTPError as error:
        return

    else:
        if response.status_code == 200:
            
            conn=createConnection()
            c=conn.cursor()
            if tagName:
                sql="INSERT INTO words (word, datetime, tag) VALUES (?, ?, ?)"
                c.execute(sql, (query, datetime.now(), tagName))
            if not tagName:
                sql="INSERT INTO words (word, datetime) VALUES (?, ?)"
                c.execute(sql, (query, datetime.now()))
            conn.commit()

            print(Panel(f"[bold green]{query}[/bold green] added to the vocabulary builder list with the tag: [blue]{tagName}[/blue]"))




    
# todo @anay: add proper docstrings     ✅
def set_mastered(query: str):
    """
    Sets the word as mastered.
    
    Args:
        query (str): Word which is to be set as mastered.
    """
    conn=createConnection()
    c=conn.cursor()
    
    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 1))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] is already marked as mastered.")
        return
    
    
    c.execute("UPDATE words SET mastered=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold green]mastered[/bold green]. Good work!")
    else:
        print(f"[bold blue]{query}[/bold blue] not in vocabulary builder list. Please look it up first. ")
    


# todo @anay: add proper docstrings      ✅
def set_unmastered(query: str):
    """
    Sets the word as unmastered.
    
    Args:
        query (str): Word which is to be set as unmastered.
    """
    conn=createConnection()
    c=conn.cursor()
    
    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 0))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] was never mastered.")
        return
    
    c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold red]unmastered[/bold red]. Remember to practice it.")
    else:
        print(f"[bold blue]{query}[/bold blue] not in vocabulary builder list. Please look it up first. ")
        


# todo @anay: Write PyTest case for this function 
def count_total_mastered():
    """
    Counts the total number of words mastered.
    """
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT COUNT(DISTINCT word) FROM words WHERE mastered=1")
    rows=c.fetchall()
    count=rows[0][0]
    print(f"You have mastered [bold green]{count}[/bold green] words.")
   
   
# todo @anay: Write PyTest case for this function 
def count_total_learning():
    """
    Counts the total number of words in vocabulary builder list that are not mastered
    """
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT COUNT(DISTINCT word) FROM words WHERE mastered=0")
    rows=c.fetchall()
    count=rows[0][0]
    print(f"You have [bold red]{count}[/bold red] words in your vocabulary builder list.")
    
    


# todo @atharva: keep recalling function until dictionary definition is found. Do not return undefined words.
def get_random_word_definition_from_api():
    """
    Gets a random word from the random-words package. 
    """
    random_word=RandomWords().get_random_word()
    print(f"A Random Word for You: {random_word}")
    definition(random_word)
            

# todo @anay: add proper docstrings         ✅
def get_random_word_from_learning_set(tag:Optional[str]=None):
    """Gets a random word from the vocabulary builder list.

    Args:
        tag (Optional[str], optional): Tag from which the random word should be. Defaults to None.
    """
        
    conn=createConnection()
    c=conn.cursor()
    if tag:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=0 ORDER BY RANDOM() LIMIT 1", (tag,))
    if not tag:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=0 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have mastered all the words in the vocabulary builder list.")
    else:
        for row in rows:
            print(f"A Random Word for You: {row[0]}")
            # Uncomment the below line to get the definition of the word as well
            # definition(row[0])
      
     
# todo @anay: add proper docstrings      ✅       
def get_random_word_from_mastered_set(tag:Optional[str]=None):
    """Gets a random word with definition from the mastered words list.

    Args:
        tag (Optional[str], optional): Tag from which the mastered word should be. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()
    if tag:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=1 ORDER BY RANDOM() LIMIT 1", (tag,))
    if not tag:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have not mastered any words yet.")
    else:
        for row in rows:
            print(f"A Random Word for You: {row[0]}")
            # Uncomment the below line to get the definition of the word as well
            # definition(row[0])

        

          
# todo @anay: write function to select all words in the database     ✅
# todo @anay: add proper docstrings     ✅
def show_list(tag=None, mastered=False, learning=False):
    """By default gets all the words in the vocabulary builder list. Otherwise, gets the words based on the arguments passed.

    Args:
        tag (string, optional): Gets the list of words of the mentioned tag. Defaults to None.
        mastered (bool, optional): If True, gets list of mastered words. Defaults to False.
        learning (bool, optional): If True, gets list of learning words. Defaults to False.
    """
    conn=createConnection()
    c=conn.cursor()

    if tag is not None and mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=1", (tag,))
    elif tag is not None and learning:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=0", (tag,))
    elif mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1")
    elif learning:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=0")
    elif tag is not None:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=?", (tag,))
    else:
        c.execute("SELECT DISTINCT word FROM words")
    
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have not searched any words yet.")
    else:
        for row in rows:
            print(f"Word: {row[0]}")
            


