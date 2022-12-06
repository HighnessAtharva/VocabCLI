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


def revise_words(
    number: Optional[int] = 10,
    tag: Optional[str] = None,
    timer: Optional[int] = 3,
    shuffle: Optional[bool] = False
):
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT DISTINCT (word) FROM words where learning=1")
    if c.fetchone():
        rows=c.fetchall()
        for row in rows:
            print(definition(row[0]))
            time.sleep(timer)
            if typer.confirm("Set as mastered?"):
                set_mastered(row[0])


    else:
        print("No words to revise. Add some words to your learning list first by using 'learn' command.")