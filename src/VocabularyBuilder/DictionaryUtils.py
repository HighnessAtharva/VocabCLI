from Database import *

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
            
fetchWordHistory("star")