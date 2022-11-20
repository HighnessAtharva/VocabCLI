import sqlite3
from sqlite3 import Error
from datetime import datetime
from rich import print


def createConnection():
    """ create a database connection to a SQLite database VocabularyBuilder.db """
    conn = None
    try:
        conn = sqlite3.connect('VocabularyBuilder.db')
    except Error as e:
        print(e)
    return conn


def createTables(conn: sqlite3.Connection):
    words=""" CREATE TABLE IF NOT EXISTS words (
	word	TEXT,
	datetime timestamp NOT NULL,
	tag	TEXT
    );
    """
    
    try:
        c = conn.cursor()
        c.execute(words)
    except Error as e:
        print(e)
   
    
def initializeDB():
    conn=createConnection()
    createTables(conn)
    

            
    



    
    