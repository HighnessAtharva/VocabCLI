import os
import json
import requests
import typer
import questionary
import random
import time
from Dictionary import *
from Exceptions import *
from typing import *
from Utils import *
from Database import createConnection, createTables
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from questionary import Style

#####################
# REVISE FUNCTIONS #         
#####################

def start_revision(c, is_collection: bool = False):
    if rows := c.fetchall():
        for count,row in enumerate(rows, start=1):
            print(Panel(
            title=f"[reverse]Revising word: [bold green]{count} / {len(rows)}[/bold green][/reverse]",
            title_align="center",
            renderable=f"{len(rows)-count} word(s) to go. Keep revising! 🧠"
            ))
            definition(row[0])

            if is_collection and not check_learning(row[0]):
                print( Panel(f"Set [bold blue]{row[0]}[/bold blue] as [bold green]learning[/bold green] ?"))
                if sure := typer.confirm(""):
                    set_learning(row[0])
                else:
                    print(Panel(f"OK, not setting [bold blue]{row[0]}[/bold blue] as learning, you can always revise it via our collection ✍🏼"))
                    print("\n\n")
                
            # if word is not mastered then prompt user to set it as mastered
            elif not check_mastered(row[0]):
                print(Panel(f"Set [bold blue]{row[0]}[/bold blue] as [bold green]mastered[/bold green] ?"))
                if sure := typer.confirm(""):
                    set_mastered(row[0])
                else:
                    print(Panel(f"OK, not setting [bold blue]{row[0]}[/bold blue] as mastered, keep learning. ✍🏼"))
                    print("\n\n")

            else:
                print("Press Y to Stop Revision. Enter to continue 📖")
                if not (sure := typer.confirm("")):
                    continue
                print(Panel("OK, stopping revision. 🛑"))
                break
    else:
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="No words to revise in the selected category. Look up some more words first by using 'define' command.")
        )
        

def revise_all(number: Optional[int] = None):  # sourcery skip: remove-redundant-if
    conn=createConnection()
    c=conn.cursor()
    
    # checks if there are any words in the database and breaks out if there are none
    if count_all_words()==0:
        return
    
    if not number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM()")
        start_revision(c)
    
    elif number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM() LIMIT ?", (number,))
        start_revision(c)
        
def revise_tag(
    number: Optional[int] = None,
    tag: Optional[str] = None
    ):  # sourcery skip: remove-redundant-if

    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if tag is not found
    if tag:
        if count_tag(tag) == 0:
            return     
            
    if tag and not number:    
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM()", (tag,))
        start_revision(c)
    
    elif number and tag:           
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM() LIMIT ?", (tag, number))
        start_revision(c)
    

def revise_learning(
    number: Optional[int] = None,
    learning: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if

    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if learning:
        if count_learning()==0:
            return 
        
    if learning and not number:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM()")
        start_revision(c)
        
    elif number and learning:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_revision(c)
        
        

def revise_mastered(
    number: Optional[int] = None,
    mastered: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if
    
    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if mastered:
        if count_mastered() ==0:
            return
        
    if mastered and not number:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM()")
        start_revision(c)
        
    elif number and mastered:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_revision(c)
        
        
def revise_favorite(
    number: Optional[int] = None,
    favorite: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if
    
    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if favorite:
        if count_favorite() ==0:
            return 
        
    if favorite and not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_revision(c)
        
    elif number and favorite:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_revision(c)
        
def revise_collection(
    number: Optional[int] = None,
    collectionName: Optional[str] = None
):
    conn=createConnection()
    c=conn.cursor()
        
    if collectionName and not number:
        c.execute("SELECT word FROM collections where collection=? ORDER BY RANDOM()", (collectionName,))
        start_revision(c, is_collection=True)
        
    elif number and collectionName:
        c.execute("SELECT word FROM collections where collection=? ORDER BY RANDOM() LIMIT ?", (collectionName, number))
        start_revision(c, is_collection=True)

#####################
# QUIZ FUNCTIONS #      
#####################
def start_quiz(c, collection=None):    # sourcery skip: remove-redundant-if
        
    if not (rows := c.fetchall()):
        return
    # break out if -n < 4
    if len(rows) < 4:
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="Not enough words to start a quiz. ❌")
        )
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

        print(Panel.fit(
            title=f"[reverse]Question [bold green]#{count}/{len(rows)}[/bold green][/reverse]",
            title_align="center",
            padding=(1, 1),
            renderable=f"Choose the correct definition for: [bold u blue]{quiz_word}[/bold u blue]"
            )
        )

        # answer
        correct_definition=one_line_definition(quiz_word)

        # question list with the correct answer
        choices=[correct_definition]


        # if taking quiz on a collection then only fake choices from the collection otherwise the answer will be obvious
        if collection:
            c.execute("SELECT DISTINCT word FROM collections where collection=? and word!=? ORDER BY RANDOM() LIMIT 3", (collection, quiz_word,))
            
        # adding 3 fake choices from words in the database.
        else:
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

        if (user_choice==correct_definition):
            score+=1
            print(Panel(f"✅ Correct! Score: [bold green]{score}[/bold green]"))
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
    c.close()         
        
def quiz_all(number: Optional[int] = None):  # sourcery skip: remove-redundant-if
    conn=createConnection()
    c=conn.cursor()
    
    # checks if there are any words in the database and breaks out if there are none
    if count_all_words()==0:
        return
    
    if not number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM()")
        start_quiz(c)
    
    elif number:
        c.execute("SELECT DISTINCT word FROM words ORDER BY RANDOM() LIMIT ?", (number,))
        start_quiz(c)

def quiz_tag(
    number: Optional[int] = None,
    tag: Optional[str] = None
    ):  # sourcery skip: remove-redundant-if

    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if tag is not found
    if tag:
        if count_tag(tag)==0:
            return     
            
    if tag and not number:    
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM()", (tag,))
        start_quiz(c)
    
    elif number and tag:           
        c.execute("SELECT DISTINCT word FROM words where tag=? ORDER BY RANDOM() LIMIT ?", (tag, number))
        start_quiz(c)
    

def quiz_learning(
    number: Optional[int] = None,
    learning: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if

    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if learning:
        if count_learning() ==0:
            return
        
    if learning and not number:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM()")
        start_quiz(c)
        
    elif number and learning:
        c.execute("SELECT DISTINCT word FROM words where learning=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_quiz(c)
        
        

def quiz_mastered(
    number: Optional[int] = None,
    mastered: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if
    
    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if mastered:
        if count_mastered() == 0:
            return
        
    if mastered and not number:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM()")
        start_quiz(c)
        
    elif number and mastered:
        c.execute("SELECT DISTINCT word FROM words where mastered=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_quiz(c)
        
        
def quiz_favorite(
    number: Optional[int] = None,
    favorite: Optional[bool] = False
    ):  # sourcery skip: remove-redundant-if
    
    conn=createConnection()
    c=conn.cursor()
    
    # will stop the execution if no words learning
    if favorite:
        if count_favorite() ==0:
            return
        
    if favorite and not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_quiz(c)
        
    elif number and favorite:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_quiz(c)

    
# todo - quiz will break and throw an error if words in the collection are not available in the api definition. Also, quiz_collection will be generally slow because it has to fetch the definition for each word in the option, find a way to make it fast.     
def quiz_collection(
    number: Optional[int] = None,
    collectionName: Optional[str] = None
):
    conn=createConnection()
    c=conn.cursor()
    
        
    if collectionName and not number:
        c.execute("SELECT word FROM collections where collection=? ORDER BY RANDOM()", (collectionName,))
        start_quiz(c, collection=collectionName)
        
    elif number and collectionName:
        c.execute("SELECT word FROM collections where collection=? ORDER BY RANDOM() LIMIT ?", (collectionName, number))
        if c.fetchone() is None:
            print(f"Collection '{collectionName}' is empty")
            return
        start_quiz(c, collection=collectionName)