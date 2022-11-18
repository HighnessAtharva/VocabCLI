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


def connectToApi(query:str="hello"):
    """_summary_: Connects to the API and returns the response in JSON format.

    Args:
        query (str, optional): _description_. Defaults to "hello".

    Returns:
        _type_: _description_
    """
    
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        response.raise_for_status()
    
    except exceptions.ConnectionError as error:
        print("Error: You are not connected to the internet.")
    
    except exceptions.HTTPError as error:
        print("We do not have the definition for that word")
    
    except exceptions.Timeout as error:
        print("Error: Timeout")

    else:
        if response.status_code == 200:
            return response.json()[0]
 
 
        
def definition(query:str, short:Optional[bool]=False):
    """_summary_: Prints the definition of the word. 

    Args:
        query (str): _description_
        short (Optional[bool], optional): _description_. Defaults to False.
    """
    if not (response := connectToApi(query)):
        return
    
    print(f"[blue]{query}[/blue]\n")
    phonetic(query)
    print("\n[bold]DEFINITION: [/bold]\n")
    if short:
        for meaningNumber in response["meanings"]:
            for meaning in meaningNumber["definitions"][:1]:
                print(f"{meaningNumber['partOfSpeech']}: {meaning['definition']}")
                
    if not short:
        for meaningNumber in response["meanings"]:
            print(meaningNumber["partOfSpeech"])
            for count, meaning in enumerate(meaningNumber["definitions"], start=1):
                print(f"{count}. {meaning['definition']}")            
            print("\n")
            


def phonetic(query: str):
    """_summary_: Prints the phonetic of the word.

    Args:
        query (str): _description_
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
                
        
        
def pronounce(query: str):
    """_summary_: Pronounces the word. Downloads the audio file, plays it and deletes it.

    Args:
        query (str): _description_
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
        
def fetchWordHistory(word):
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
            


def tag(query: str, tagName:Optional[str]=None):
    """_summary_: Tags the word in the vocabulary builder list.

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