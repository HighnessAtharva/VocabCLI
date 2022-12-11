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

def start_revision(c):
    if rows := c.fetchall():
        for count,row in enumerate(rows, start=1):
            print(Panel(f"Revising word: [bold green]{count}[/bold green] / [bold green]{len(rows)}[/bold green]"))
            definition(row[0])
            if typer.confirm(f"Set {row[0]} as mastered?"):
                set_mastered(row[0])
            
    else:
        print(Panel("No words to revise in the selected category. Look up some more words first by using 'define' command."))
        

def revise_all(number: Optional[int] = None):  # sourcery skip: remove-redundant-if
    conn=createConnection()
    c=conn.cursor()
    
    # checks if there are any words in the database and breaks out if there are none
    count_all_words()
    
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
        count_tag(tag)     
            
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
        count_learning() 
        
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
        count_mastered() 
        
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
        count_favorite() 
        
    if favorite and not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_revision(c)
        
    elif number and favorite:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_revision(c)

#####################
# QUIZ FUNCTIONS #      
#####################
def start_quiz(c):    # sourcery skip: remove-redundant-if
        
    if not (rows := c.fetchall()):
        return
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
        
def quiz_all(number: Optional[int] = None):  # sourcery skip: remove-redundant-if
    conn=createConnection()
    c=conn.cursor()
    
    # checks if there are any words in the database and breaks out if there are none
    count_all_words()
    
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
        count_tag(tag)     
            
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
        count_learning() 
        
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
        count_mastered() 
        
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
        count_favorite() 
        
    if favorite and not number:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM()")
        start_quiz(c)
        
    elif number and favorite:
        c.execute("SELECT DISTINCT word FROM words where favorite=1 ORDER BY RANDOM() LIMIT ?", (number,))
        start_quiz(c)

    
