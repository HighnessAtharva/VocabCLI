import calendar
import glob
import os
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

################################
# VISUALIZATION FUNCTIONS
################################


def viz_top_words_bar(N: int = 10, popup: bool = False) -> None:
    """
    Visualize the top N words looked up by the user

    1. Get the top N words and their word count from the database and store them in a list
    2. If no words are found, print an error message and return
    3. If there are less words than the number we want to display, print a warning message
    4. Create a dataframe from the list
    5. Set the style of the graph
    6. Plot the graph
    7. Export the graph to a png file
    8. If popup is True, show the graph in a popup window

    Args:
        N (int, optional): Number of words to visualize. Defaults to 10.
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    # get top N words
    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC LIMIT ?",
        (N,),
    )
    rows = c.fetchall()

    top_words = [row[0] for row in rows if row[0] is not None]
    count = [row[1] for row in rows if row[1] != 0]

    if not top_words:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="No words found ❌",
            )
        )
        return

    if len(top_words) < N:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🔺 Not enough words found. Showing graph for available words only. 📊",
            )
        )

    # create a dataframe
    df = pd.DataFrame(
        list(zip(top_words, count)), index=count, columns=["Word Lookup Count", "Count"]
    )

    sns.set_style("dark")

    # plot the dataframe
    graph = sns.barplot(
        x="Word Lookup Count",
        y="Count",
        data=df,
        palette="pastel",
        ax=plt.subplots(figsize=(12, 10))[1],
        edgecolor="0.4",
    )

    graph.set_title(
        f"Top {len(top_words)} Most Looked Up Words",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    graph.set_xlabel(
        "Words",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_ylabel(
        "Lookup Count",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_xticklabels(
        graph.get_xticklabels(),
        rotation=40,
        ha="right",
        fontname="MS Gothic",
        color="black",
        fontweight="bold",
    )
    # graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    plt.savefig("exports/GRAPH-top_words_bar.png")
    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable=f"Displaying [bold u]Bar graph[/bold u] of [gold1]top {len(top_words)} words[/gold1] 📊",
                padding=(1, 1),
            )
        )
        plt.show()


def viz_top_tags_bar(N: int = 10, popup: bool = False) -> None:
    """
    Visualizes the top N tags with the most words.

    1. Get the top N tags and their word count from the database and store them in a list
    2. If no words are found, print an error message and return
    3. If there are less words than the number we want to display, print a warning message
    4. Create a dataframe from the list
    5. Set the style of the graph
    6. Plot the graph
    7. Export the graph to a png file
    8. If popup is True, show the graph in a popup window


    Args:
        N (int, optional): Number of top tags to visualize . Defaults to 10.
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    # get top N tags
    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?",
        (N,),
    )
    rows = c.fetchall()

    top_tags = [row[0] for row in rows if row[0] is not None]
    count = [row[1] for row in rows if row[1] != 0]

    if not top_tags:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="No tags found ❌",
            )
        )
        return

    if len(top_tags) < N:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🔺 Not enough tags found. Showing graph for available tags only. 📊",
            )
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=["Tag", "Count"])

    sns.set_style("dark")

    # plot the dataframe
    graph = sns.barplot(
        x="Tag",
        y="Count",
        data=df,
        palette="pastel",
        ax=plt.subplots(figsize=(12, 12))[1],
        edgecolor="0.4",
    )

    graph.set_title(
        f"Top {len(top_tags)} Tags",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    graph.set_xlabel(
        "Tags",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_ylabel(
        "Word Count",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_xticklabels(
        graph.get_xticklabels(),
        rotation=0,
        ha="right",
        fontname="MS Gothic",
        color="black",
        fontweight="bold",
    )
    # graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    # show the plot
    plt.grid()

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    plt.savefig("exports/GRAPH-top_tags_bar.png")
    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable=f"Displaying [bold u]Bar graph[/bold u] of [gold1]top {len(top_tags)} tags[/gold1] 📊",
                padding=(1, 1),
            )
        )
        plt.show()


def viz_top_words_pie(N: int = 10, popup: bool = False) -> None:
    """
    Visualizes the top N words with the most lookups.

    1. Create a cursor and execute a query to fetch the word and the count of the word from the database
    2. If no words are found, print an error message and return
    3. If there are less words than the number we want to display, print a warning message
    4. Create a dataframe using the top words and their counts
    5. Create a pie chart using matplotlib and seaborn and save it to a file
    6. If the popup parameter is True, display the pie chart using matplotlib

    Args:
        N (int, optional): Number of top words to visualize . Defaults to 10.
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY COUNT(*) DESC LIMIT ?",
        (N,),
    )
    rows = c.fetchall()

    top_words = [row[0] for row in rows if row[0] is not None]
    count = [row[1] for row in rows if row[1] != 0]

    if not top_words:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="No words found ❌",
            )
        )
        return

    if len(top_words) < N:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🔺 Not enough words found. Showing pie chart for available words only. 📊",
            )
        )

    # create a dataframe
    df = pd.DataFrame(
        list(zip(top_words, count)), index=count, columns=["Word Lookup Count", "Count"]
    )
    plt.clf()
    plt.pie(
        df["Count"],
        labels=df["Word Lookup Count"],
        autopct="%1.1f%%",
        startangle=90,
        labeldistance=1.15,
        textprops={"fontsize": 12, "color": "black", "fontname": "Candara","fontweight":"bold"},
    )
    sns.set_style("dark")
    plt.title(
        f"Top {len(top_words)} Words",
        fontsize=38,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )

    # saving the plot
    plt.savefig("exports/GRAPH-top_words_pie.png")

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable=f"Displaying [bold u]Pie Chart[/bold u] of [gold1]top {len(top_words)} words[/gold1]",
                padding=(1, 1),
            )
        )
        plt.show()


def viz_top_tags_pie(N: int = 10, popup: bool = False) -> None:
    """
    Visualizes the top N tags with the most words.

    1. Execute a SQL query to get the count of each tag. The query returns a list of tuples, where the first element is the tag and the second is the count.
    2. If no words are found, print an error message and return
    3. If there are less words than the number we want to display, print a warning message
    4. Create a dataframe from the list of tags and the list of counts.
    5. Set the theme of the plot.
    6. Create a pie chart using the dataframe.
    7. Save the plot in a file.
    8. Check if the directory exists, if not create it.
    9. Show the plot on screen if the popup argument is true.

    Args:
        N (int, optional): Number of top tags to visualize . Defaults to 10.
    """

    # get top N tags
    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT tag, COUNT(*) FROM words WHERE tag is NOT NULL GROUP BY tag ORDER BY COUNT(*) DESC LIMIT ?",
        (N,),
    )
    rows = c.fetchall()

    top_tags = [row[0] for row in rows if row[0] is not None]
    count = [row[1] for row in rows if row[1] != 0]

    if not top_tags:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="No tags found ❌",
            )
        )
        return

    if len(top_tags) < N:
        print(
            Panel(
                title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable="🔺 Not enough tags found. Showing Pie Chart for available tags only. 📊",
            )
        )

    # create a dataframe
    df = pd.DataFrame(list(zip(top_tags, count)), index=count, columns=["Tag", "Count"])
    sns.set_style("dark")

    plt.clf()

    plt.title(
        f"Top {len(top_tags)} Tags",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )

    plt.pie(
        x=df["Count"],
        labels=df["Tag"],
        autopct="%1.1f%%",
        startangle=90,
        labeldistance=1.15,
        textprops={"fontsize": 12, "color": "black", "fontname": "Candara","fontweight":"bold"},
    )

    # saving the plot
    plt.savefig("exports/GRAPH-top_tags_pie.png")

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable=f"Displaying [bold u]Pie Chart[/bold u] of [gold1]top {len(top_tags)} tags[/gold1] 📊",
                padding=(1, 1),
            )
        )
        plt.show()


# BUG days of the week is buggy, week range is not properly set
def words_distribution_week_util() -> tuple[list, list]:
    """
    Returns the distribution of words by day of the week.

    1. Create a dictionary with numbers as keys and weekdays as values.
    2. Create two lists, one for weekdays and one for word count.
    3. Query the database for word count for each day in the current week.
    4. Loop through the results and assign the weekday to the list.
    5. Assign the word count to the list.
    6. Return the two lists.

    Returns:
        list: list of days of the week.
        list: list of days of the word counts.
    """

    conn = createConnection()
    c = conn.cursor()

    days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    word_count = [0, 0, 0, 0, 0, 0, 0]

    # get word count for each day in current week
    c.execute(
        "select strftime('%d/%m/%Y', datetime) as date, count(word) from words WHERE datetime>=datetime('now', '-7 days') GROUP BY date"
    )

    rows = c.fetchall()
    for row in rows:
        date = datetime.strptime(row[0], "%d/%m/%Y")
        days_of_week_index = date.weekday()
        word_count[days_of_week_index] = row[1]
        
    # rotate both the lists to start from Sunday 
    days_of_week = days_of_week[6:] + days_of_week[:6]
    word_count = word_count[6:] + word_count[:6]

    return days_of_week, word_count


# BUG 🐞 Graph does not show the entire week
def viz_word_distribution_week(popup: bool = False) -> None:
    """
    Visualizes the distribution of words by day of the week.

    1. Create a dataframe from a list of tuples (day, count).
    2. Set the style of the graph.
    3. Plot the graph with the dataframe.
    4. Set the title, x and y labels, x and y ticks.
    5. Save the graph.
    5. Show the graph in a popup window if popup is True.

    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    days_of_week, word_count = words_distribution_week_util()

    # create a dataframe
    df = pd.DataFrame(list(zip(days_of_week, word_count)), columns=["Day", "Count"])

    sns.set_style("dark")
    # plot the dataframe
    graph = sns.barplot(
        x="Day",
        y="Count",
        data=df,
        palette="pastel",
        ax=plt.subplots(figsize=(12, 10))[1],
        edgecolor="0.4",
    )

    graph.set_title(
        "Words Distribution by Week",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    graph.set_xlabel(
        "Day",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_ylabel(
        "Count",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_xticklabels(graph.get_xticklabels(), ha="right",
        fontname="MS Gothic",
        color="black",
        fontweight="bold")
    # graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')
    
    plt.yticks(np.arange(min(word_count), max(word_count)+1, max(word_count)/10))
    plt.grid()

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    plt.savefig("exports/GRAPH-words_distribution_week.png")

    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable="Displaying [bold u]Bar Graph[bold u] of [gold1]weekly word lookup[/gold1] distribution. 📊",
                padding=(1, 1),
            )
        )
        plt.show()


def word_distribution_month_util() -> tuple[list, list]:
    """
    Returns the distribution of word by dates of month.

    1. Determine current year, current month and next month.
    2. Determine total number of days in current month.
    3. Get unformatted datestrings for each day in current month.
    4. Get word count for each day in current month.

    Returns:
        list: List of dates of month.
        list: List of word counts.
    """

    conn = createConnection()
    c = conn.cursor()

    # determine current year, current month and next month [INT]
    year = datetime.now().year
    month = datetime.now().month
    month_next = datetime.now().month + 1
    if month_next == 13:
        month_next = 1
        increment_year = True
    else:
        increment_year = False

    # determine total number of days in current month [INT]
    total_days = calendar.monthrange(year, month)[1]
    word_count = [None] * total_days

    # get unformatted datestrings for each day in current month
    current_month = f"{str(year)}-{str(month)}"
    if len(current_month) == 6:
        current_month = f"{str(year)}-0{str(month)}"

    if len(str(month_next)) == 1:
        month_next = f"0{str(month_next)}"
    next_month = f"{str(year+1 if increment_year else year)}-{str(month_next)}"

    dates = np.arange(current_month, next_month, dtype="datetime64[D]").tolist()

    dates = [date.strftime("%d %b, %Y") for date in dates]

    # get word count for each day in current month
    c.execute(
        "select strftime('%d', datetime) as date, count(word) as word_count from words WHERE date(datetime)>=date('now', 'start of month') GROUP BY date"
    )
    rows = c.fetchall()
    for row in rows:
        index = int(row[0]) - 1
        word_count[index] = row[1]

    # drop all the None values
    dates = [date for date in dates if date is not None]
    word_count = [count for count in word_count if count is not None]
    return dates, word_count


def viz_word_distribution_month(popup: bool = False) -> None:
    """
    Visualizes the distribution of words by dates of month.

    1. Get the data from the function word_distribution_month_util() which is a list of:
        a. Dates
        b. Word count
    2. Create a dataframe from the list
    3. Set the style of the graph
    4. Plot the graph
    5. Set the graph title, x and y axis labels, and x axis tick labels
    6. Save the graph to the folder 'exports'
    7. If popup is True, show the graph in a popup window

    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    dates, word_count = word_distribution_month_util()
    # print(dates)

    # create a dataframe
    df = pd.DataFrame(list(zip(dates, word_count)), columns=["Date", "Count"])

    sns.set_style("dark")
    # plot the dataframe
    graph = sns.barplot(
        x="Date",
        y="Count",
        data=df,
        palette="pastel",
        ax=plt.subplots(figsize=(12, 8))[1],
        edgecolor="0.4",
    )

    graph.set_title(
        "Word Distribution by Month",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    graph.set_xlabel(
        "Date",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_ylabel(
        "Count",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_xticklabels(
        graph.get_xticklabels(),
        rotation=30,
        ha="right",
        fontname="MS Gothic",
        color="black",
        fontweight="bold",
    )
    # graph.set_yticklabels(graph.get_yticklabels(), fontname='Candara',color='black')

    plt.tight_layout()
    plt.grid()

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    plt.savefig("exports/GRAPH-word_distribution_month.png")
    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable="Displaying [bold u]Bar Graph[/bold u] of [gold1]monthly word lookup[/gold1] distribution. 📊",
                padding=(1, 1),
            )
        )
        plt.show()


def viz_learning_vs_mastered(popup: bool = False) -> None:
    """
    Visualizes the distribution of words by learning and mastered.

    1. Count number of words in learning and mastered.
    2. Set the style of the graph.
    3. Plot a pie chart.
    4. Export the graph as png.
    5. Show the graph in a popup window if popup=True.

    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    conn = createConnection()
    c = conn.cursor()

    c.execute("select count(DISTINCT word) from words WHERE learning = 1")
    learning_count = c.fetchone()[0]

    c.execute("select count(DISTINCT word) from words WHERE mastered = 1")
    mastered_count = c.fetchone()[0]

    # set plot style: grey grid in the background:
    sns.set(style="dark")

    # set the figure size
    plt.figure(figsize=(14, 14))

    # top bar -> sum all values(learning and mastered) to find y position of the bars
    top_bar = [learning_count]
    bottom_bar = [mastered_count]

    x = [""]
    plt.bar(x, bottom_bar, color="darkblue")
    plt.bar(x, top_bar, bottom=bottom_bar, color="lightblue")

    # add legend
    top_bar = mpatches.Patch(color="darkblue", label="mastered words")
    bottom_bar = mpatches.Patch(color="lightblue", label="learning words")
    plt.legend(handles=[top_bar, bottom_bar])

    plt.title(
        "Learning Vs Mastered Words",
        fontsize=30,
        fontweight="bold",
        pad=25,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    plt.ylabel(
        "Words",
        fontsize=25,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    # plt.ylabel('Count', fontsize=15, fontweight='bold', labelpad=20, color='black', fontname='MS Gothic')

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    # show the graph
    plt.savefig("exports/GRAPH-learning_vs_mastered.png")
    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable="Displaying [bold u]Stacked Bar Graph[/bold u] of [gold1]mastered vs learning words[/gold1] 📊",
                padding=(1, 1),
            )
        )
        plt.show()


def viz_word_distribution_category(popup: bool = False) -> None:
    """
    Visualizes the distribution of words by category.

    1. Selects the collection column and the word count from the words and collections table.
    2. Creates a dataframe from the data obtained.
    3. Sets the style of the graph.
    4. Creates a bar graph based on the dataframe.
    5. Saves the graph to the exports folder.
    6. Displays graph if popup is True.

    Args:
        popup (bool, optional): Whether to show the graph in a popup window. Defaults to False.
    """

    conn = createConnection()
    c = conn.cursor()

    # inner join the words and collections table to get the word count from each category
    c.execute(
        "select collections.collection ,COUNT(DISTINCT words.word)from words inner join collections on words.word=collections.word GROUP BY collections.collection ORDER BY COUNT(DISTINCT words.word) DESC"
    )

    # To get the actual words themselves based on their category uncomment this
    # c.execute("select DISTINCT words.word, collections.collection from words inner join collections on words.word=collections.word")

    rows = c.fetchall()
    category = [row[0] for row in rows]
    word_count = [row[1] for row in rows]

    # plot a bar graph based on the word count and category
    df = pd.DataFrame(
        list(zip(category, word_count)), columns=["Category", "Word Count"]
    )

    sns.set_style("dark")
    # plot the dataframe
    graph = sns.barplot(
        x="Category",
        y="Word Count",
        data=df,
        palette="pastel",
        ax=plt.subplots(figsize=(12, 8))[1],
        edgecolor="0.4",
    )

    graph.set_title(
        "Word Distribution by Category",
        fontsize=30,
        fontweight="bold",
        pad=20,
        color="black",
        loc="center",
        fontname="Constantia",
    )
    graph.set_xlabel(
        "Word Count",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_ylabel(
        "Collection",
        fontsize=20,
        fontweight="bold",
        labelpad=20,
        color="black",
        fontname="MS Gothic",
    )
    graph.set_xticklabels(
        graph.get_xticklabels(),
        rotation=40,
        ha="right",
        fontname="MS Gothic",
        color="black",
        fontweight="bold",
    )
    # y axis labels ticks interval should be 1
    graph.set_yticks(np.arange(0, int(max(word_count)), 50))

    plt.tight_layout()
    plt.grid()

    # check if the directory exists, if not create it
    if not os.path.exists("exports"):
        os.makedirs("exports")

    plt.savefig("exports/GRAPH-word_distribution_category.png")
    if popup:
        print(
            Panel(
                title="[b reverse green]  Graph  [/b reverse green]",
                renderable="Displaying [bold u]Bar Graph[/bold u] of [gold1]word distribution by category[/gold1] 📊",
                padding=(1, 1),
            )
        )
        plt.show()


# TODO: Graph related to complexity or difficulty? ✅
