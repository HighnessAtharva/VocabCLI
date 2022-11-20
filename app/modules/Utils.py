from random_word import RandomWords
from typing import *
from datetime import datetime
from rich import print

from Database import createConnection, createTables

# todo @anay: add proper docstrings
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
       

# todo @anay: add proper docstrings
def add_tag(query: str, tagName:Optional[str]=None):
    """
    Tags the word in the vocabulary builder list.

    Args:
        query (str): _description_
        tagName (Optional[str], optional): _description_. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()
    if tagName:
        sql="INSERT INTO words (word, datetime, tag) VALUES (?, ?, ?)"
        c.execute(sql, (query, datetime.now(), tagName))
    if not tagName:
        sql="INSERT INTO words (word, datetime) VALUES (?, ?)"
        c.execute(sql, (query, datetime.now()))
    conn.commit()
    
    print(f"[bold green]{query}[/bold green] added to the vocabulary builder list with the tag: [blue]{tagName}[/blue]")
  
    
# todo @anay: add proper docstrings
def set_mastered(query: str):
    """
    Sets the word as mastered.
    
    Args:
        query (str): _description_
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
   
    

# todo @anay: add proper docstrings
def set_unmastered(query: str):
    """
    Sets the word as unmastered.
    
    Args:
        query (str): _description_
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
    c.execute("SELECT COUNT (DISTINCT word) FROM words WHERE mastered=1")
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
    print(f"You are learning [bold green]{count}[/bold green] words")
    

   

# todo @atharva: keep recalling function until dictionary definition is found. Do not return undefined words.
def get_random_word_definition_from_api():
    """
    Gets a random word from the random-words package. 
    """
    random_word=RandomWords().get_random_word()
    print(f"A Random Word for You: {random_word}")
    definition(random_word)
            

# todo @anay: add proper docstrings
def get_random_word_from_learning_set(tag:Optional[str]=None):
    """Gets a random word from the vocabulary builder list.

    Args:
        tag (Optional[str], optional): _description_. Defaults to None.
    """
        
    conn=createConnection()
    c=conn.cursor()
    if tag:
        c.execute("SELECT word FROM words WHERE tag=? AND mastered=0 ORDER BY RANDOM() LIMIT 1", (tag,))
    if not tag:
        c.execute("SELECT word FROM words WHERE mastered=0 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have mastered all the words in the vocabulary builder list.")
    else:
        for row in rows:
            print(f"A Random Word for You: {row[0]}")
            definition(row[0])
      
     
# todo @anay: add proper docstrings       
def get_random_word_from_mastered_set(tag:Optional[str]=None):
    """Gets a random word with definition from the mastered words list.

    Args:
        tag (Optional[str], optional): _description_. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()
    if tag:
        c.execute("SELECT word FROM words WHERE tag=? AND mastered=1 ORDER BY RANDOM() LIMIT 1", (tag,))
    if not tag:
        c.execute("SELECT word FROM words WHERE mastered=1 ORDER BY RANDOM() LIMIT 1")
    rows=c.fetchall()
    if len(rows) <= 0:
        print("You have not mastered any words yet.")
    else:
        for row in rows:
            print(f"A Random Word for You: {row[0]}")
            definition(row[0])
            
            
# todo @anay: write function to select all words in the database
# todo @anay: add proper docstrings 
def show_list(favorite=False, learning=False, mastered=False, tag=False, date=False, last=None):
    conn=createConnection()
    c=conn.cursor()
    def show_favorite_list():
        c.execute("SELECT word FROM words WHERE favorite=1")
        rows=c.fetchall()
        if len(rows) <= 0:
            print("You have no favorite words yet.")
        else:
            for row in rows:
                print(row[0]) 
    
    def show_learning_list():
        c.execute("SELECT word FROM words WHERE mastered=1")
        rows=c.fetchall()
        if len(rows) <= 0:
            print("You aren't learning any words currently.")
        else:
            for row in rows:
                print(row[0]) 
    
    def show_mastered_list():
        pass
    
    def show_tag_list():
        pass
    
    def show_date_list():
        pass
    
    def show_last_list(last=10):
        pass
    
    if favorite:
        show_favorite_list()
    if learning:
        show_learning_list()
    if mastered:
        show_mastered_list()
    if tag:
        show_tag_list()
    if date:
        show_date_list()
    if last:
        show_last_list(last)
    
    if(not favorite and not learning and not mastered and not tag and not date and not last):
        # show all the words    
        conn=createConnection()
        c=conn.cursor()
        c.execute("SELECT word FROM words")
        rows=c.fetchall()
        if len(rows) <= 0:
            print("You have no favorite words yet.")
        else:
            for row in rows:
                print(row[0]) 