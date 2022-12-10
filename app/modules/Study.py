import os
import json
import requests
import typer
from typing import *
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from random_word import RandomWords
from Database import createConnection, createTables
from rich.console import Console
from rich.table import Table
from Dictionary import *
from Exceptions import *
from datetime import datetime, timedelta
from Utils import *
import questionary
import random
import time
from questionary import Style


def revise_words(
    number: Optional[int] = None,
    tag: Optional[str] = None
):  # sourcery skip: remove-redundant-if
    """Revise words from learning list in a one by one fashion prompting user to set a word as mastered.

    Args:
        number (Optional[int], optional): Limit numbers to revise an displays words in random (non-ascending order). Defaults to None.
        tag (Optional[str], optional): Revise words of a specific tag. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()

    # handle only number
    if number and not tag:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM() LIMIT ?", (number,))

    # handle only tag
    elif tag and not number:
        c.execute("SELECT DISTINCT word FROM words where tag=? and learning=1 ORDER BY word ASC", (tag,))

    # handle both number and tag
    elif number and tag:
        c.execute("SELECT DISTINCT word FROM words where tag=? and learning=1 ORDER BY RANDOM() LIMIT ?", (tag, number))

    # handle neither number nor tag (default) ie. all words in learning list in alphabetical order
    elif not tag and not number:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY word ASC")


    if rows := c.fetchall():
        for count,row in enumerate(rows, start=1):
            print(Panel(f"Revising word: [bold green]{count}[/bold green] / [bold green]{len(rows)}[/bold green]"))
            definition(row[0])
            if typer.confirm(f"Set {row[0]} as mastered?"):
                set_mastered(row[0])
            
    else:
        print(Panel("No words to revise. Add some words to your learning list first by using 'learn' command."))


    

def start_quiz(
    number: Optional[int] = None,
    tag: Optional[str] = None
):    # sourcery skip: remove-redundant-if
    """Start a quiz session (single correct choice). Display total score at the end of the quiz.

    Args:
        number (Optional[int], optional): Limit numbers to revise an displays words in random (non-ascending order). Defaults to None.
        tag (Optional[str], optional): Revise words of a specific tag. Defaults to None.
    """
    conn=createConnection()
    c=conn.cursor()

    # handle only number
    if number and not tag:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM() LIMIT ?", (number,))

    # handle only tag
    elif tag and not number:
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY word ASC", (tag,))

    # handle both number and tag
    elif number and tag:
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM() LIMIT ?", (tag, number))

    # handle neither number nor tag (default) ie. quiz on all words in alphabetical order
    elif not tag and not number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY word ASC")
    
    
    if rows := c.fetchall():
        # break out if -n < 4
        if len(rows) < 4:
            print(Panel("Not enough words to start a quiz. Look up some more words first by using 'define' command."))
            return
        
        
        # setting quiz style
        fancy_style = Style([
            ('qmark', 'fg:#673ab7 bold'),       
            ('question', 'fg:#0000ff bold'),    
            ('answer', 'fg:#ffff00 bold'),      
            ('pointer', 'fg:#ffd700 bold'),     
            ('highlighted', 'fg:#0000ff bold'), 
            ('selected', 'fg:#cc5454'),         
            ('separator', 'fg:#cc5454'),        
            ('instruction', 'fg:#673ab7 bold'),                
        ])

        # initializing score and timer
        score=0
        tic = datetime.now()
        
        # iterating over questions
        for count,row in enumerate(rows, start=1):   
            
            # setting up question
            quiz_word=row[0]
            
            print(Panel(
                title=f"[reverse]Question [bold green]#{count}/{len(rows)}[/bold green][/reverse]",
                title_align="center",
                renderable=f"Choose the correct definition for: [bold u blue]{quiz_word}[/bold u blue]"
                )
            )
            
            
            # answer
            correct_definition=one_line_definition(quiz_word)
            
            # question list with the correct answer
            choices=[correct_definition]
            
            # adding 3 fake choices from words in the database. 
            c.execute("SELECT DISTINCT word FROM words where word!=? ORDER BY RANDOM() LIMIT 3", (quiz_word,))
            choices.extend(one_line_definition(row[0]) for row in c.fetchall())
            random.shuffle(choices)
            
            
            user_choice=questionary.select(
                f"",
                choices=choices,
                style=fancy_style,
                show_selected=True,
                use_arrow_keys=True,
                use_indicator=True,
                qmark='',
                instruction=' '
            ).ask()
            
            if(user_choice==correct_definition):
                score+=1
                print(Panel(f"✅ Correct! Score: [bold green]{score}[/bold green]"))
                print("\n\n")
            else:
                print(Panel(f"❌ Incorrect! Score: [bold green]{score}[/bold green]\nCorrect answer was: [bold green]{correct_definition}[/bold green]"))
                print("\n\n")
                
        toc = datetime.now()
        diff = toc - tic

        seconds = diff.seconds
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(Panel.fit(title="[b reverse white]  Quiz completed!  [/b reverse white]", 
                    title_align="center",
                    padding=(1, 1),
                    renderable=f"🎯 [bold bright_magenta u]Score[/bold bright_magenta u]: [bold green]{score}[/bold green] / [bold green]{len(rows)}[/bold green]\n⏰ [bold bright_magenta u]Time Elapsed[/bold bright_magenta u]: [blue]{minutes:0.0f}M {seconds:0.0f}S[/blue]")
            )            
        