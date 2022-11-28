# import libraries
import seaborn as sns
import matplotlib.pyplot as plt 
import pandas as pd
import calendar
import numpy as np
from datetime import datetime
from modules.Database import *



# function to visualize top N tags with the most words
def viz_top_tags(N=10):
    # get top N tags
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_tags=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]
    
    if not top_tags:
        print("No tags found")
        return
    
    if len(top_tags) < N:
        print("Not enough tags found. Showing graph for available tags only.")
    
    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=['Tag', 'Count'])

    sns.set_style("dark")
    
    # plot the dataframe
    graph=sns.barplot(x='Tag', y='Count', data=df, palette='pastel',ax=plt.subplots(figsize=(12, 10))[1])

    # set the title
    graph.set(title=f'Top {N} Tags', xlabel='Tags', ylabel='Count')

    # show the plot
    plt.grid() 
    plt.show()
    

# todo function to visualize top distribution of words by date [day, week, month]
def words_distribution_week():
    pass

def word_distribution_month_util():
    conn=createConnection()
    c=conn.cursor()

    # determine current year, current month and next month [INT]
    year=datetime.now().year
    month=datetime.now().month
    month_next=datetime.now().month+1
    
    # determine total number of days in current month [INT]
    total_days=calendar.monthrange(year, month)[1]
    word_count=[0]*total_days

    # get unformatted datestrings for each day in current month
    current_month = f"{str(year)}-{str(month)}"
    next_month = f"{str(year)}-{str(month_next)}"
    dates=np.arange(current_month, next_month, dtype='datetime64[D]').tolist()
    dates=[date.strftime("%d %b, %Y") for date in dates]
    
    # get word count for each day in current month
    c.execute("select strftime('%d', datetime) as date, count(word) as word_count from words WHERE date(datetime)>=date('now', 'start of month') GROUP BY date")
    rows=c.fetchall()
    for row in rows:
        index=int(row[0])-1
        word_count[index]=row[1]
        
    return dates, word_count
    
def word_distribution_month():
    dates, word_count=word_distribution_month_util()
    # print(dates)
    
    # create a dataframe
    df = pd.DataFrame(list(zip(dates, word_count)),  columns=['Date', 'Count'])
    
    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Date', y='Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 10))[1])

    # set the title
    graph.set(title='Words Distribution by Month', xlabel='Date', ylabel='Count')
    
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right")
    plt.tight_layout()
    plt.grid() 
    plt.show()

    
viz_top_tags()   
word_distribution_month()



def word_distribution_year():    
    pass

# todo function to vizualize trend of learning and mastered words in a given time period [day, week, month] -> USE COMPOSITE BAR GRAPH

# todo function to visualize most looked up words [top 10] with the number of times looked up

