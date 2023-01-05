import calendar
import glob
from datetime import datetime
from tkinter import *

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from Database import *
from PIL import Image, ImageTk
from rich.panel import Panel

# TODO: - revise docstrings and add wherever missing. 
# TODO: - add type hints wherever missing and return types as well
# TODO: @anay - add rich themes, styling, formatting, emojis for almost every print statement. 


################################
# VISUALIZATION FUNCTIONS
################################
def viz_top_words_bar(N:int=10, popup:bool=False):
    """Visualize the top N words looked up by the user
    
    Args:
        N (int, optional): Number of words to visualize. Defaults to 10.
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """
    
    # get top N words
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_words=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_words:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="No words found ❌")
        )
        return

    if len(top_words) < N:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="⚠ Not enough words found. Showing graph for available words only. 📊")
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_words, count)), index=count, columns=['Word Lookup Count', 'Count'])

    sns.set_style("dark")

    # plot the dataframe
    graph=sns.barplot(x='Word Lookup Count', y='Count', data=df, palette='pastel',ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    graph.set_title(f'Top {len(top_words)} Most Looked Up Words', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Words', fontsize=15, fontweight='bold', labelpad=-10, color='black', fontname='MS Gothic')
    graph.set_ylabel('Lookup Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right", fontname='Candara', color='black', fontweight='700')
    #graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()
    plt.savefig('exports/GRAPH-top_words_bar.png')
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
                        renderable=f"Displaying [bold u]Bar graph[/bold u] of [gold1]top {len(top_words)} words[/gold1] 📊",
                        padding=(1, 1)))
        plt.show()


def viz_top_tags_bar(N:int=10, popup:bool=False):
    """
    Visualizes the top N tags with the most words.

    Args:
        N (int, optional): Number of top tags to visualize . Defaults to 10.
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    # get top N tags
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_tags=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_tags:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="No tags found ❌")
        )
        return

    if len(top_tags) < N:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="⚠ Not enough tags found. Showing graph for available tags only. 📊")
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=['Tag', 'Count'])

    sns.set_style("dark")

    # plot the dataframe
    graph=sns.barplot(x='Tag', y='Count', data=df, palette='pastel',ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    
    graph.set_title(f'Top {len(top_tags)} Tags', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Tags', fontsize=15, fontweight='bold', labelpad=-8, color='black', fontname='MS Gothic') 
    graph.set_ylabel('Word Count',fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right", fontname='Candara', color='black')
    #graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()
    plt.savefig('exports/GRAPH-top_tags_bar.png')
    if popup:    
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
                    renderable=f"Displaying [bold u]Bar graph[/bold u] of [gold1]top {len(top_tags)} tags[/gold1] 📊",
                    padding=(1, 1)))
        plt.show()


def viz_top_words_pie(N:int=10, popup:bool=False):
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_words=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_words:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="No words found ❌")
        )
        return

    if len(top_words) < N:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="⚠ Not enough words found. Showing pie chart for available words only. 📊")
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_words, count)), index=count, columns=['Word Lookup Count', 'Count'])
    plt.clf()
    plt.pie(df['Count'], labels=df['Word Lookup Count'], autopct='%1.1f%%', startangle=90, labeldistance=1.15, textprops={'fontsize': 10, 'color': 'black', 'fontname': 'Candara'})
    sns.set_style("dark")
    plt.title(f'Top {len(top_words)} Words', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia')
    
    # saving the plot
    plt.savefig('exports/GRAPH-top_words_pie.png')
    
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
            renderable=f"Displaying [bold u]Pie Chart[/bold u] of [gold1]top {len(top_words)} words[/gold1]",
            padding=(1, 1)))
        plt.show()
    
def viz_top_tags_pie(N:int=10, popup:bool=False):
    """
    Visualizes the top N tags with the most words.

    Args:
        N (int, optional): Number of top tags to visualize . Defaults to 10.
    """

    # get top N tags
    conn=createConnection()
    c=conn.cursor()
    c.execute("SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?", (N,))
    rows=c.fetchall()

    top_tags=[row[0] for row in rows if row[0] is not None]
    count= [row[1] for row in rows if row[1] != 0]

    if not top_tags:
        print(Panel(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="No tags found ❌")
        )
        return

    if len(top_tags) < N:
        print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]", 
                title_align="center",
                padding=(1, 1),
                renderable="⚠ Not enough tags found. Showing Pie Chart for available tags only. 📊")
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=['Tag', 'Count'])
    sns.set_style("dark")

    plt.clf()
    
    plt.title(f'Top {len(top_tags)} Tags', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 

    plt.pie(x=df['Count'], labels=df['Tag'], autopct='%1.1f%%', startangle=90, labeldistance=1.15, textprops={'fontsize': 10, 'color': 'black', 'fontname': 'Candara'})
        
    # saving the plot
    plt.savefig('exports/GRAPH-top_tags_pie.png')
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
                    renderable=f"Displaying [bold u]Pie Chart[/bold u] of [gold1]top {len(top_tags)} tags[/gold1] 📊",
                    padding=(1, 1)))
        plt.show()


# BUG days of the week is buggy, week range is not properly set
def words_distribution_week_util():
    """
    Returns the distribution of words by day of the week.

    Returns:
        list: list of days of the week.
        list: list of days of the word counts.
    """

    conn=createConnection()
    c=conn.cursor()

    days={0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    days_of_week=[None]*7
    word_count=[None]*7

    # get word count for each day in current week
    c.execute("select strftime('%d/%m/%Y', datetime) as date, count(word) from words WHERE datetime>=datetime('now', '-7 days') GROUP BY date")

    rows=c.fetchall()
    for index, row in enumerate(rows):
        date=datetime.strptime(row[0], "%d/%m/%Y")
        days_of_week[index]=days.get(date.weekday())
        word_count[index]=row[1]

    return days_of_week, word_count

# BUG 🐞 Graph does not show the entire week
def viz_word_distribution_week(popup:bool=False):
    """
    Visualizes the distribution of words by day of the week.

    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    days_of_week, word_count=words_distribution_week_util()

    # create a dataframe
    df = pd.DataFrame(list(zip(days_of_week, word_count)),  columns=['Day', 'Count'])

    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Day', y='Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 10))[1], edgecolor='0.4')

    graph.set_title('Words Distribution by Week', fontsize=18, fontweight='bold', pad=20, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Day', fontsize=15, fontweight='bold', labelpad=10, color='black', fontname='MS Gothic')
    graph.set_ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), fontname='Candara', color='black')
    #graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')
    
    plt.grid()
    
    plt.savefig('exports/GRAPH-words_distribution_week.png')
    if popup:    
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
                    renderable="Displaying [bold u]Bar Graph[bold u] of [gold1]weekly word lookup[/gold1] distribution. 📊",
                    padding=(1, 1)))
        plt.show()



def word_distribution_month_util():
    """
    Returns the distribution of word by dates of month.

    Returns:
        list: List of dates of month.
        list: List of word counts.
    """

    conn=createConnection()
    c=conn.cursor()

    # determine current year, current month and next month [INT]
    year=datetime.now().year
    month=datetime.now().month
    month_next=datetime.now().month+1
    if month_next==13:
        month_next=1
        increment_year=True

    # determine total number of days in current month [INT]
    total_days=calendar.monthrange(year, month)[1]
    word_count=[None]*total_days

    # get unformatted datestrings for each day in current month
    current_month = f"{str(year)}-{str(month)}"
    if len(str(month_next))==1:
        month_next=f"0{str(month_next)}"
    next_month = f"{str(year+1 if increment_year else year)}-{str(month_next)}"

    dates=np.arange(current_month, next_month, dtype='datetime64[D]').tolist()
    
    dates=[date.strftime("%d %b, %Y") for date in dates]
    
    # get word count for each day in current month
    c.execute("select strftime('%d', datetime) as date, count(word) as word_count from words WHERE date(datetime)>=date('now', 'start of month') GROUP BY date")
    rows=c.fetchall()
    for row in rows:
        index=int(row[0])-1
        word_count[index]=row[1]

    return dates, word_count


def viz_word_distribution_month(popup:bool=False):
    """ 
    Visualizes the distribution of words by dates of month. 
    
    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.    
    """

    dates, word_count=word_distribution_month_util()
    # print(dates)

    # create a dataframe
    df = pd.DataFrame(list(zip(dates, word_count)),  columns=['Date', 'Count'])

    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Date', y='Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 8))[1], edgecolor='0.4')


    graph.set_title('Word Distribution by Month', fontsize=18, fontweight='bold', pad=5, color='black', loc='center', fontname='Constantia') 
    graph.set_xlabel('Date', fontsize=15, fontweight='bold', labelpad=0, color='black', fontname='MS Gothic')
    graph.set_ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right",fontname='Candara', color='black')
    #graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')
    
    plt.tight_layout()
    plt.grid()
    
    plt.savefig('exports/GRAPH-word_distribution_month.png')
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
                    renderable="Displaying [bold u]Bar Graph[/bold u] of [gold1]monthly word lookup[/gold1] distribution. 📊",
                    padding=(1, 1)))
        plt.show()


def word_distribution_year_util():

    pass

def viz_word_distribution_year(popup:bool=False):
    
    pass

def viz_learning_vs_mastered(popup:bool=False):
    """ 
    Visualizes the distribution of words by learning and mastered. 
    
    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.    
    """    

    conn=createConnection()
    c=conn.cursor()
    
    c.execute("select count(DISTINCT word) from words WHERE learning = 1")
    learning_count=c.fetchone()[0]
    
    c.execute("select count(DISTINCT word) from words WHERE mastered = 1")
    mastered_count=c.fetchone()[0]
   
    # set plot style: grey grid in the background:
    sns.set(style="dark")

    # set the figure size
    plt.figure(figsize=(14, 14))

    # top bar -> sum all values(learning and mastered) to find y position of the bars
    top_bar = [learning_count]
    bottom_bar = [mastered_count]
    
    x = ['']
    plt.bar(x, bottom_bar, color='darkblue')
    plt.bar(x, top_bar, bottom=bottom_bar, color='lightblue')

    # add legend
    top_bar = mpatches.Patch(color='darkblue', label='mastered words')
    bottom_bar = mpatches.Patch(color='lightblue', label='learning words')
    plt.legend(handles=[top_bar, bottom_bar])

    plt.title('Word Distribution by Month', fontsize=18, fontweight='bold', pad=5, color='black', loc='center', fontname='Constantia') 
    plt.xlabel('Date', fontsize=15, fontweight='bold', labelpad=0, color='black', fontname='MS Gothic')
    #plt.ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    
    # show the graph
    plt.savefig('exports/GRAPH-learning_vs_mastered.png')
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
            renderable="Displaying [bold u]Stacked Bar Graph[/bold u] of [gold1]mastered vs learning words[/gold1] 📊",
            padding=(1, 1)))
        plt.show()
    

def viz_word_distribution_category(popup:bool=False):
    conn=createConnection()
    c=conn.cursor()
    
    # inner join the words and collections table to get the word count from each category
    c.execute("select collections.collection ,COUNT(DISTINCT words.word)from words inner join collections on words.word=collections.word GROUP BY collections.collection ORDER BY COUNT(DISTINCT words.word) DESC")
    
    # To get the actual words themselves based on their category uncomment this
    # c.execute("select DISTINCT words.word, collections.collection from words inner join collections on words.word=collections.word")
    
    rows=c.fetchall()
    category=[row[0] for row in rows]
    word_count= [row[1] for row in rows]
    
    # plot a bar graph based on the word count and category
    df = pd.DataFrame(list(zip(category, word_count)),  columns=['Category', 'Word Count'])

    sns.set_style("dark")
    # plot the dataframe
    graph=sns.barplot(x='Category', y='Word Count', data=df, palette='pastel', ax=plt.subplots(figsize=(12, 8))[1], edgecolor='0.4')
    
    graph.set_title('Word Distribution by Category', fontsize=18, fontweight='bold', pad=5, color='black', loc='center', fontname='Constantia')
    graph.set_xlabel('Word Count', fontsize=15, fontweight='bold', labelpad=0, color='black', fontname='MS Gothic')
    graph.set_ylabel('Collection', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')
    graph.set_xticklabels(graph.get_xticklabels(), rotation=40, ha="right",fontname='Candara', color='black')
    # y axis labels ticks interval should be 1
    graph.set_yticks(np.arange(0, int(max(word_count)), 1))
 
    plt.tight_layout()
    plt.grid()
    
    plt.savefig('exports/GRAPH-word_distribution_category.png')
    if popup:
        print(Panel(title="[b reverse green]  Graph  [/b reverse green]",
            renderable="Displaying [bold u]Bar Graph[/bold u] of [gold1]word distribution by category[/gold1] 📊",
            padding=(1, 1)))
        plt.show()


# TODO: Graph related to complexity or difficulty? ✅

