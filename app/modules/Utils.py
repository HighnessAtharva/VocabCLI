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
        print("[bold red]You have not searched for this word before.[/bold red]")
    else:
        count=len(rows)
        if count==1:
            print(f"You have searched for [bold]{word}[/bold] {count} time before.")
        else:
            print(f"You have searched for [bold]{word}[/bold] {count} times before.")
        for row in rows:
            history=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M:%S')
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
    
    # check if word is set to learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        c.execute("UPDATE words SET learning=0 WHERE word=?", (query,))
    
    
    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 1))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] is already marked as mastered.")
        return
    
    
    c.execute("UPDATE words SET mastered=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold green]mastered[/bold green]. Good work!")



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

        

def set_learning(query: str):
    """
    Sets the word as learning.
    
    Args:
        query (str): Word which is to be set as learning.
    """
    conn=createConnection()
    c=conn.cursor()
    

    # check if word is already mastered
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 1))
    if c.fetchone():
        # TODO add a typer prompt to ask if the user wants to move word from mastered to learning
        c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
        
    
    
    # check if word is already learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] is already marked as learning.")
        return
    
    c.execute("UPDATE words SET learning=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold green]learning[/bold green]. Keep revising!")



def set_unlearning(query: str):
    """
    Sets the word as unlearning.
    
    Args:
        query (str): Word which is to be set as unlearning.
    """
    conn=createConnection()
    c=conn.cursor()
        
    # check if word is not already unlearned
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 0))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] was never learning.")
        return    
        
    # check if word is already learning
    c.execute("SELECT * FROM words WHERE word=? and learning=?", (query, 1))
    if c.fetchone():
        c.execute("UPDATE words SET learning=0 WHERE word=?", (query,))
        
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold red]unlearning[/bold red].")    



def set_favorite(query: str):
    """
    Sets the word as favorite.
    
    Args:
        query (str): Word which is to be set as favorite.
    """
    conn=createConnection()
    c=conn.cursor()
    
    # check if word is already favorite
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 1))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] is already marked as favorite.")
        return
    
    c.execute("UPDATE words SET favorite=1 WHERE word=?", (query,))
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been set as [bold green]favorite[/bold green].")


    
def set_unfavorite(query:str):
    """
    Remove the word from favorite list.
    
    Args:
        query (str): Word which is to be removed from favorite.
    """
    conn=createConnection()
    c=conn.cursor()
        
    # check if word was never favorited
    c.execute("SELECT * FROM words WHERE word=? and favorite=?", (query, 0))
    if c.fetchone():
        print(f"[bold blue]{query}[/bold blue] was never favorite.")
        return    
        
    # set word to favorite
    c.execute("UPDATE words SET favorite=0 WHERE word=?", (query,))
        
    if c.rowcount > 0:
        conn.commit()
        print(f"[bold blue]{query}[/bold blue] has been removed from [bold red]favorite[/bold red].")   
        

    
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
# FIXME : debug only tag argument   
def show_list(favorite=False,learning=False, mastered=False, tag=None, date=None, last=10):
    """Gets all the words in the vocabulary builder list.
    
    Args:
        favorite (bool, optional): If True, gets list of favorite words. Defaults to False.
        learning (bool, optional): If True, gets list of learning words. Defaults to False.
        mastered (bool, optional): If True, gets list of mastered words. Defaults to False.
        tag (string, optional): Gets the list of words of the mentioned tag. Defaults to None.
        date (string, optional): Get a list of words from a particular date. Defaults to None.
        last (string, optional):"Get a list of n last searched words. Defaults to 10.
    """
    conn=createConnection()
    c=conn.cursor()

    if tag and mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=1", (tag,))
        error_message="You have not mastered any words with this tag yet."
    elif tag and learning:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND learning=1", (tag,))
        error_message="You have not added any words with this tag to the vocabulary builder list yet."
    elif tag and favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND favorite=1", (tag,))
        error_message="You have not added any words with this tag to the favorite list yet."
    elif mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1")
        error_message="You have not mastered any words yet."
    elif learning:
        c.execute("SELECT DISTINCT word FROM words WHERE learning=1")
        error_message="You have not added any words to the learning list yet."
    elif favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1")
        error_message="You have not added any words to the favorite list yet."
    elif date:
        c.execute("SELECT DISTINCT word FROM words WHERE datetime=?", (date,))
        error_message="No records found within this date range"
    elif last:
        c.execute("SELECT DISTINCT word FROM words ORDER BY datetime DESC LIMIT ?", (last,))
        error_message="You haven't searched for any words yet."
    elif tag:
        c.execute("SELECT word FROM words WHERE tag=?", (tag,))
        error_message="No words found with this tag."
    # default case when no arguments are passed
    # elif tag==None and mastered==False and learning==False and favorite==False and date==None and last==10:
    #     c.execute("SELECT DISTINCT word FROM words")
    #     error_message="You haven't searched for any words yet."
    else:
        error_message="Invalid arguments passed. You cannot pair those together. "
        
    
    
    rows=c.fetchall()
    if len(rows) <= 0:
        print(error_message)
    else:
        for row in rows:
            print(f"Word: {row[0]}")
    
# todo - @atharva: function to delete all word from the database
def delete_all():
    pass

# todo - @atharva: function to delete mastered words from the database
def delete_mastered():
    pass

# todo - @atharva: function to delete learning words from the database
def delete_learning():
    pass

# todo - @atharva: function to delete favorite words from the database
def delete_favorite():
    pass

# todo - @atharva: function to delete words of the last n days from the database
def delete_days(days: int):
    pass


# todo - @atharva: function to delete words from a particular tag from the database
def delete_words_from_tag(tag: str):
    pass



