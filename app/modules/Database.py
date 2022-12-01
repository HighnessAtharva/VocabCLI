import sqlite3
from sqlite3 import Error
from datetime import datetime
from rich import print


def createConnection():
    """ 
    Creates a database connection to a SQLite database VocabularyBuilder.db 
    
    Returns: 
        Connection object or None.    
    """
    conn = None
    try:
        conn = sqlite3.connect('./VocabularyBuilder.db')
    except Error as e:
        print(e)
    return conn


def createTables(conn: sqlite3.Connection):
    """ 
    Creates tables in the database 
    
    Args:
        conn (sqlite3.Connection): Connection object
    """

    words="""CREATE TABLE IF NOT EXISTS "words" (
	"word"	TEXT,
	"datetime"	timestamp NOT NULL UNIQUE,
	"tag"	TEXT,
	"mastered"	INTEGER NOT NULL DEFAULT 0,
	"learning"	INTEGER NOT NULL DEFAULT 0,
	"favorite"	INTEGER NOT NULL DEFAULT 0
);
    """
    
 
    try:
        c = conn.cursor()
        c.execute(words)
    except SQLException as e:
        print(e)
   
    
def initializeDB():
    """ Initializes the database """

    conn=createConnection()
    createTables(conn)