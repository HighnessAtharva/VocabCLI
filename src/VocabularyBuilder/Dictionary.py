import os
import json
import requests
from playsound import playsound
from pathlib import Path
from requests import exceptions
from typing import *
from Database import *
from datetime import datetime
from rich import print
from random_word import RandomWords



# todo @anay: add proper docstrings
def connectToApi(query:str="hello"):
    """
    Connects to the API and returns the response in JSON format.

    Args:
        query (str, optional): Word to lookup to test the API. Defaults to "hello".

    Returns:
        dict: Response in JSON format
    """
    
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()
    
    except exceptions.ConnectionError as error:
        print("[bold red]Error: You are not connected to the internet.[/bold red]")
    
    except exceptions.HTTPError as error:
        print("[bold red]We do not have the definition for that word[/bold red]")
        
    except exceptions.Timeout as error:
        print("[bold red]Error: Timeout[/bold red]")

    else:
        if response.status_code == 200:
            return response.json()[0]
 
 
# todo @anay: add proper docstrings 
# todo @anay: Refer typer/rich docs and add table formatting to the output      
def definition(query:str, short:Optional[bool]=False):
    """
    Prints the definition of the word. 

    Args:
        query (str): _description_
        short (Optional[bool], optional): _description_. Defaults to False.
    """
    if not (response := connectToApi(query)):
        return 0
    
    print(f"[blue]{query}[/blue]\n")
    phonetic(query)
    print("\n[bold]DEFINITION: [/bold]\n")
    if short:
        for meaningNumber in response["meanings"]:
            for meaning in meaningNumber["definitions"][:1]:
                
                # Noun: definition
                print(f"{meaningNumber['partOfSpeech']}: {meaning['definition']}")
                
    if not short:
        for meaningNumber in response["meanings"]:
            # Part of Speech: Noun/Verb/Adjective
            print(meaningNumber["partOfSpeech"])
            for count, meaning in enumerate(meaningNumber["definitions"], start=1):
                # 1. Meaning EYXAKSJKSDJ
                # 2. Meaning ASKDJASJD
                # table row begins
                print(f"{count}. {meaning['definition']}")  
                # table row ends          
            print("\n")
            

# todo @anay: add proper docstrings
def phonetic(query: str):
    """
    Prints the phonetic of the word.

    Args:
        query (str): word for which phonetic is to be printed
    """
    if not (response := connectToApi(query)):
        return
    if len(response["phonetics"])==0:
        phonetic="[bold red]Phonetic Unavailable[/bold red]"
    else:
        for phonetics in response["phonetics"]:
            if "text" in phonetics and len(phonetics["text"])>0:
                phonetic= phonetics["text"];     
            else:
                phonetic= "[bold red]Phonetic Unavailable[/bold red]"
    print(f"{phonetic}")
                
        
# todo @anay: add proper docstrings      
def pronounce(query: str):
    """
    Pronounces the word. Downloads the audio file, plays it and deletes it.

    Args:
        query (str): word to be pronounced
    
    """
    if not (response := connectToApi(query)):
        return
    if len(response["phonetics"])==0:
        print("Audio Unavailable")
    else:
        phonetic = response["phonetics"][0] if "phonetics" in response else "phonetics not available"
        audioURL=phonetic["audio"] if "audio" in phonetic else None
        if audioURL not in [None, ""]:
            audio = requests.get(audioURL, allow_redirects=True)
            open(f'{query}.mp3', 'wb').write(audio.content)
            playsound(os.path.join(Path().cwd(), f"{query}.mp3"))
            # playsound(f'{Path().cwd()}/{query}.mp3')
            print("Audio played")
            os.remove(f"{query}.mp3") if os.path.exists(f"{query}.mp3") else None
        else:
            print("Audio Unavailable")
       
        
# todo @anay: add proper docstrings
def fetchWordHistory(word):
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
def tag(query: str, tagName:Optional[str]=None):
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
    c.execute("SELECT COUNT(*) FROM words WHERE mastered=1")
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
    c.execute("SELECT COUNT(*) FROM words WHERE mastered=0")
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
def get_all_words():
    pass

# todo @anay: write function to select all words with a particular tag. Argument is required!
# todo @anay: add proper docstrings
def get_words_of_tag(tag: str):
    pass

# todo @anay: write function to select all words from learning list, filter by tag if tag is provided. Tag is optional.
# todo @anay: add proper docstrings
def get_words_from_learning_list(tag:Optional[str]=None):
    pass

# todo @anay: write function to select all words from mastered list, , filter by tag if tag is provided. Tag is optional.
# todo @anay: add proper docstrings  
def get_words_from_mastered_list(tag:Optional[str]=None):
    pass