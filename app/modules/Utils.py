import contextlib
import os
import json
import requests
from playsound import playsound
from pathlib import Path
from requests import exceptions
from typing import *
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from random_word import RandomWords
from Database import createConnection, createTables
from rich.console import Console
from rich.table import Table
from Dictionary import connect_to_api, definition
from Exceptions import *
from datetime import datetime, timedelta

def check_word_exists(query: str):
    conn= createConnection()
    c=conn.cursor()
    # check if word exists in the database
    with contextlib.suppress(WordNeverSearchedException):
        c.execute("SELECT * FROM words WHERE word=?", (query,))
        if not c.fetchone():
            raise WordNeverSearchedException(query)
        return True
        

def fetch_word_history(word: str):
    """ Fetches all instances of timestamp for a word from the database 

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
            raise WordNeverSearchedException
        count=len(rows)
        if count==1:
            print(Panel(f"You have searched for [bold]{word}[/bold] {count} time before. 🔎"))
        else:
            print(Panel(f"You have searched for [bold]{word}[/bold] {count} times before. 🔎"))
        for row in rows:
            history=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            table.add_row(history)
            table.add_section() 
        print(table)
    except WordNeverSearchedException as e:
        print(e)
        
fetch_word_history("hello")
def add_tag(query: str, tagName:str):
    """
    Tags the word in the vocabulary builder list.

    Args:
        query (str): Word which is to be tagged.
        tagName (Optional[str], optional): Tag name which is to be added to the word and inserts it into the database. Defaults to None.
    """
     
    # check if word definitions exists. If yes, add to database otherwise do not do anything. Don't even print anything.    
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()
            
    except exceptions.HTTPError as error:
        print(Panel(f"The word [bold red]{query}[/bold red] is not a valid word. Please check the spelling. 🤔"))
        return

    else:
        if response.status_code == 200:
            
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
                print(Panel(f"[bold blue]{query}[/bold blue] tag has been changed to [bold green]{tagName}[/bold green]. ✅"))
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
    
    
    # check if word is set to learning
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
        print(Panel(f"[bold blue]{query}[/bold blue] has been set as [bold red]learning[/bold red]. Remember to practice it."))

        
        
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
    c.execute("SELECT * FROM words WHERE word=? and mastered=?", (query, 1))
    if c.fetchone():
        # TODO add a typer prompt to ask if the user wants to move word from mastered to learning
        c.execute("UPDATE words SET mastered=0 WHERE word=?", (query,))
    
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
        print(Panel(f"[bold blue]{query}[/bold blue] is already marked as favorite. 💙"))
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
 

def count_all_words()->int:
    """Counts the distinct number of words in the database

    Returns:
        int: Total word count
    """   
    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words"
    c.execute(sql)
    rows=c.fetchall()
    return len(rows)    

    
def count_mastered()->int:
    """ Counts the distinct number of mastered words in the database

    Returns:
        int: Total mastered word count
    """
    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE mastered=1"
    c.execute(sql)
    rows=c.fetchall()
    return len(rows)    
    

def count_learning()->int:
    """ Counts the distinct number of learning words in the database

    Returns:
        int: Total learning word count
    """
    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE learning=1"
    c.execute(sql)
    rows=c.fetchall()
    return len(rows)

def count_favorite()->int:
    """ Counts the distinct number of favorite words in the database

    Returns:
        int: Total favorite word count
    """
    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE favorite=1"
    c.execute(sql)
    rows=c.fetchall()
    return len(rows)

def count_tag(tag:str)->int:
    """ Counts the distinct number of words in the database with a particular tag

    Returns:
        int: Total word count of specific tag
    """
    conn=createConnection()
    c=conn.cursor()
    sql="SELECT DISTINCT word FROM words WHERE tag=?"
    c.execute(sql, (tag,))
    rows=c.fetchall()
    return len(rows)



# todo @atharva: keep recalling function until dictionary definition is found. Do not return undefined words.
def get_random_word_definition_from_api():
    """
    Gets a random word from the random-words package. 
    """    
    random_word=RandomWords().get_random_word()
    print(Panel(f"A Random Word for You: [bold green]{random_word}[/bold green]"))
    definition(random_word)
     


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
        print(Panel("You have no words in your vocabulary builder learning list. 👀"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [bold blue]learning[/bold blue] words list: [bold blue]{row[0]}[/bold blue]"))
            # Uncomment the below line to get the definition of the word as well
            # definition(row[0])
      

    
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
        print(Panel("You have not mastered any words yet. 👀"))
    else:
        for row in rows:
            print(Panel(f"A Random word from your [bold green]mastered[/bold green] words list: [bold green]{row[0]}[/bold green]"))
            # Uncomment the below line to get the definition of the word as well
            # definition(row[0])


          
  
# FIXME @atharva: debug only tag argument 🐞
def show_list(favorite:Optional[bool]=False,learning:Optional[bool]=False, mastered:Optional[bool]=False, tag:Optional[bool]=None, date:Optional[int]=None, last:Optional[int]=None, most: Optional[int]=None):
    """Gets all the words in the vocabulary builder list.
    
    Args:
        favorite (bool, optional): If True, gets list of favorite words. Defaults to False.
        learning (bool, optional): If True, gets list of learning words. Defaults to False.
        mastered (bool, optional): If True, gets list of mastered words. Defaults to False.
        tag (string, optional): Gets the list of words of the mentioned tag. Defaults to None.
        date (string, optional): Get a list of words from a particular date. Defaults to None.
        last (string, optional):"Get a list of n last searched words. Defaults to None.
        most (string, optional): Get a list of n most searched words. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()

    # todo: arguments do not work together. Fix this. list -m -t fruits invokes commands seperately.
    if tag is not None and mastered==True:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND mastered=1", (tag,))
        success_message=f"[bold green]Mastered[/bold green] words with tag [bold green]{tag}[/bold green] are:"
        error_message="You have not mastered any words with this tag yet. ❌"

    elif tag and learning:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND learning=1", (tag,))
        success_message=f"[bold blue]Learning[/bold blue] words with tag [bold blue]{tag}[/bold blue] are:"
        error_message="You have not added any words with this tag to the vocabulary builder list yet. ❌"

    elif tag and favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=? AND favorite=1", (tag,))
        success_message=f"[bold gold1]Favorite[/bold gold1] words with tag [bold magenta]{tag}[/bold magenta] are:"
        error_message="You have not added any words with this tag to the favorite list yet. ❌"

    elif favorite and mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1 AND mastered=1")
        success_message = "[bold green]Mastered[/bold green] [bold gold1]Favorite[/bold gold1] words are:"
        error_message="You do not mastered words that are set as favorite ❌"

    elif favorite and learning:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1 AND learning=1")
        success_message = "[bold blue]Learning[/bold blue] [bold gold1]Favorite[/bold gold1] words are:"
        error_message="You do not have any learning words that are set as favorite ❌"

    elif mastered:
        c.execute("SELECT DISTINCT word FROM words WHERE mastered=1")
        success_message = "[bold green]Mastered[/bold green] words are:"
        error_message="You have not [bold green]mastered[/bold green] any words yet. ❌"

    elif learning:
        c.execute("SELECT DISTINCT word FROM words WHERE learning=1")
        success_message="[bold blue]Learning[/bold blue] words are:"
        error_message="You have not added any words to the [bold blue]learning list[/bold blue] yet. ❌"

    elif favorite:
        c.execute("SELECT DISTINCT word FROM words WHERE favorite=1")
        success_message="[bold gold1]Favorite[/bold gold1] words are:"
        error_message="You have not added any words to the [bold gold1]favorite[/bold gold1] list yet. ❌"

    elif date:
        c.execute(f"SELECT DISTINCT word FROM words where datetime > datetime('now' , '-{date} days')")
        date_today=datetime.now().strftime("%d/%m/%Y")
        date_before=datetime.now() - timedelta(days=int(date))
        success_message=f"Words added to the vocabulary builder list from [bold blue]{date_before.strftime('%d/%m/%Y')}[/bold blue] TO [bold blue]{date_today}[/bold blue] are:"
        error_message="No records found within this date range ❌"

    elif last:
        c.execute("SELECT DISTINCT word FROM words ORDER BY datetime DESC LIMIT ?", (last,))
        success_message=f"Last [bold blue]{last}[/bold blue] words searched are:"
        error_message="You haven't searched for any words yet. ❌"

    elif tag:
        c.execute("SELECT DISTINCT word FROM words WHERE tag=?", (tag,))
        success_message=f"Words with tag [bold magenta]{tag}[/bold magenta] are:"
        error_message=f"No words found with the tag {tag}. ❌"
    
    elif most:
        c.execute("SELECT word, COUNT(word) AS `word_count` FROM words GROUP BY word ORDER BY `word_count` DESC LIMIT ?", (most,))
        success_message=f"Top [bold blue]{most}[/bold blue] most searched words are:"
        error_message="You haven't searched for any words yet. ❌"
    
    elif favorite is False and learning is False and mastered is False and tag is None and date is None and last is None and most is None:
        c.execute("SELECT DISTINCT word FROM words")
        success_message="Here is your list of words: "
        error_message="You have no words in your vocabulary builder list. ❌"
    
    else:
        error_message="Invalid arguments passed. You cannot pair those together. ❌"
        

    rows=c.fetchall()
    if len(rows) <= 0:
        print(Panel(error_message))
    else:
        print(Panel(success_message))
        rows = [Panel(f"[deep_pink4]{row[0]}[deep_pink4]", expand=True) for row in rows]
        print(Columns(rows))
            
            
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
    print(Panel(f"All words[{rowcount}] [bold red]deleted[/bold red] from all your lists. ✅"))


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
    print(Panel(f"All [bold green]mastered[/bold green] words[{rowcount}] [bold red]deleted[/bold red] from your lists. ✅"))



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
    print(Panel(f"All [bold blue]learning[/bold blue] words[{rowcount}][bold red] deleted[/bold red] from your lists. ✅"))


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
    print(Panel(f"All [bold gold1]favorite[/bold gold1] words[{rowcount}][bold red] deleted[/bold red] from your lists. ✅"))



def delete_words_from_tag(tag: str):
    """Deletes all the words from a particular tag from the database."""
    conn=createConnection()
    c=conn.cursor()
            
    rowcount=count_tag(tag)
    if rowcount==0:
        print(Panel(f"[bold red]No words in tag {tag}.[/bold red] Add some first. ➕"))
        return
    
    c.execute("DELETE FROM words WHERE tag=?", (tag,))
    conn.commit()
    print(Panel(f"All words[{rowcount}] with tag [bold magenta]{tag}[/bold magenta] [bold red]deleted[/bold red] from your lists. ✅"))


def delete_word(query:str):
    """Deletes a word from the database.

    Args:
        query (str): Word to be deleted
    """
    conn=createConnection()
    c=conn.cursor()
    
    check_word_exists(query)

    sql="DELETE FROM words WHERE word=?"
    c.execute(sql, (query,))
    if c.rowcount>0:
        conn.commit()
        print(Panel(f"[bold red]Word {query} deleted[/bold red] from your lists. ✅"))
        
        
def get_learning_rate(today=False, week=False, month=False, year=False, graph=False):
    """Returns the learning rate of the user."""
    conn=createConnection()
    c=conn.cursor()
    if today:
        c.execute("SELECT word FROM words WHERE tag is NULL")
        total_words=c.fetchall()
        print(total_words)
        # # get todays learning words
        # c.execute("SELECT COUNT(DISTINCT word) FROM words WHERE learning=1 AND date(datetime)=date('now')")
        # learning_count_today=c.fetchone()[0]
        # # get yesterdays learning words
        # c.execute("SELECT COUNT(DISTINCT word) FROM words WHERE learning=1 AND date(datetime)=date('now', '-1 day')")
        # learning_count_yesterday=c.fetchone()[0]
        
        
        # print(Panel(f"[bold]Yesterday's[/bold] learning rate was [bold blue]{learning_count_yesterday}[/bold blue] words."))
        # print(Panel(f"[bold]Today[/bold] you have learned [bold blue]{learning_count_today}[/bold blue] words."))
        