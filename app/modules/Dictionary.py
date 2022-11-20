import os
import json
import requests
from playsound import playsound
from pathlib import Path
from requests import exceptions
from typing import *
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def connect_to_api(query:str="hello"):
    """
    Connects to the API and returns the response in JSON format.

    Args:
        query (str, optional): Word to lookup to test the API. Defaults to "hello".

    Returns:
        dict: Response in JSON format.
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
 
 
# todo @anay: add proper docstrings    ✅
def phonetic(query: str):
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
                phonetic= phonetics["text"];     
            else:
                phonetic= "[bold red]Phonetic Unavailable[/bold red]"
    return(phonetic)
                
                
                
# todo @anay: add proper docstrings     ✅
# todo @anay: Refer typer/rich docs and add table formatting to the output    ✅  
# FIXME @atharva: If definition is not available, message "we do not have the definition for that word" is being printed twice 🐞
# FIXME @atharva: For parts of Speech all defintions are not being printed or being printed more than once. Table formatting is right. Check indentation and loops 🐞

def definition(query:str, short:Optional[bool]=False):
    """
    Prints the definition of the word. 

    Args:
        query (str): Word which is meant to be defined.
        short (Optional[bool], optional): If True, it will print just the short definition, if False it will print the whole definition. Defaults to False.
    """
    if not (response := connect_to_api(query)):
        return 0
    
    print(Panel(f"[bold red]{query}[/bold red]"))
    print(Panel(phonetic(query)))
    print(Panel("[bold]DEFINITION: [/bold]"))
    
    if short:

        for meaningNumber in response["meanings"]:
            table=Table(show_header=True, header_style="bold magenta")
            for meaning in meaningNumber["definitions"][:1]:
                table.add_column("Part of Speech", style="dim", width=12)
                table.add_column("Definition", style="dim")
                table.add_row(meaningNumber["partOfSpeech"], meaning["definition"])
        table.add_section() 
        console = Console()
        console.print(table)
                
    if not short:
        
        for meaningNumber in response["meanings"]:
            print(Panel(f"Part of Speech:[bold blue] {meaningNumber['partOfSpeech']} [/bold blue]" ))
            for count, meaning in enumerate(meaningNumber["definitions"], start=1):
                table=Table(show_header=True, header_style="bold magenta")
                table.add_column("Sr. No.", style="dim", width=12)
                table.add_column("Definition", style="dim")
                table.add_row(f"{count}.", meaning["definition"])
                
            table.add_section()    
            console = Console()
            console.print(table)
        print("\n")  
  
      


        
# todo @anay: add proper docstrings    ✅    
def say_aloud(query: str):
    """
    Pronounces the word. Downloads the audio file, plays it and deletes it.

    Args:
        query (str): Word to be pronounced.
    
    """
    if not (response := connect_to_api(query)):
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
           
            print("Audio played")
            os.remove(f"{query}.mp3") if os.path.exists(f"{query}.mp3") else None
        else:
            print("Audio Unavailable")
