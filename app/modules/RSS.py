import feedparser
import typer
import contextlib
from Exceptions import *
from Database import createConnection, createTables
from datetime import datetime, timedelta
from pathlib import Path
from sqlite3 import *
from typing import *
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from bs4 import BeautifulSoup
from rich.progress import Progress, SpinnerColumn, TextColumn


# TODO: @anay - add rich themes, styling, formatting, emojis for almost every print statement.
# TODO: @anay - Remove Panel.fit() and replace it with Panel() where message text varies. For errors let it be Panel.fit().


def add_feed(url):
    """Add the feed to the database"""
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Adding Feed", total=None)
    # ----------------- Spinner -----------------#
        try:
            # parse the feed
            feed = feedparser.parse(url)

            # if URL is not a feed URL or does not return a 200 status code, print error message
            if feed.status != 200 or feed.bozo:
                print("Error: Feed not found")
                return
        except Exception as e:
            print("Error: Feed not found")
            return

        conn = createConnection()
        c = conn.cursor()

        # check if feed exists in the database
        c.execute("SELECT * from rss where link=?", (url,))
        if c.fetchone():
            print("Error: Feed already exists")
            return

        # add feed to database if it does not exist
        # NOTE: feed.feed.link is not the same as url, you want to store the RSS feed URL, not the website URL
        c.execute("INSERT INTO rss (title, link, description, datetime) VALUES (?, ?, ?, ?)",
                  (feed.feed.title, url, feed.feed.description, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

        # TODO: @anay - convert this to a table
        print("Feed added successfully")
        print("Title: ", feed.feed.title)
        print("Link: ", feed.feed.link)
        print("Summary:", feed.feed.description)


def get_all_feeds():
    """Get the feed details from the database"""
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Getting your feeds", total=None)
    # ----------------- Spinner -----------------#

        conn = createConnection()
        c = conn.cursor()

        # get all feeds
        c.execute("SELECT * from rss")
        rows = c.fetchall()

        # if no feeds exist, print error message
        if not rows:
            print("Error: No feeds added yet. Use 'rss' command to add a feed.")
            return

        # TODO: @anay - convert this to a table
        print("Feeds🚗")
        for row in rows:
            # do not display the RSS feed URL, display the website URL instead
            link = feedparser.parse(row[1]).feed.link
            print("Title: ", row[0])
            print("Link: ", link)
            print("Summary:", row[2])
            print("Date added:", datetime.datetime.strptime(
                row[3], "%Y-%m-%d %H:%M:%S").strftime("%d %b \'%y | %H:%M"))
            print()


def remove_feed():
    """Remove the feed from the database"""
    conn = createConnection()
    c = conn.cursor()

    # check if feed exists in the database
    c.execute("SELECT * from rss")
    rows = c.fetchall()
    if not rows:
        print("Error: Feed does not exist")
        return
    for idx, row in enumerate(rows, start=1):
        print("Title: ", row[0])
        print("Link: ", row[1])
        print("Summary:", row[2])
        print("Date added:", datetime.datetime.strptime(
            row[3], "%Y-%m-%d %H:%M:%S").strftime("%d %b \'%y | %H:%M"))
        print()

    print("Enter the index of the feed you want to remove!")
    try:
        index = int(input("Index: "))
    except ValueError:
        print("Error: index should be a number")
        return
    if index > len(rows):
        print("Error: Invalid index, out of range")
        return

    feed_name = rows[index - 1][0]
    # remove feed from database
    c.execute("DELETE FROM rss WHERE title=?", (feed_name,))
    conn.commit()
    print(f"Feed {feed_name} removed successfully")


def remove_html_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    return ' '.join(soup.stripped_strings)


def check_feed_for_new_content(title):
    """Parse the feed and check for new content"""
    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Checking feed for news...", total=None)
    # ----------------- Spinner -----------------#

        conn = createConnection()
        c = conn.cursor()
        c.execute("SELECT * from rss where title LIKE ?", (f"%{title}%",))
        # check if feed exists in the database
        rows = c.fetchall()
        if not rows:
            print(
                "Error: This feed is not added to your list. Use 'rss' command to add a feed.")
            return

        for row in rows:
            feed = feedparser.parse(row[1])
            print("Seeing updates for feed: ", row[0])

            # TODO: @anay - convert this to a table

            # sorting by reverse chronological order
            for entry in sorted(feed.entries, key=lambda x: x.published):
                published = entry.published_parsed

                # convert 8 tuple to datetime object
                published = datetime.datetime(*published[:6])
                published = published.strftime("%d %b \'%y | %H:%M")

                print(
                    f"[bold blue reverse]TITLE:[/bold blue reverse][link={str(entry.link)}]{remove_html_tags(entry.title)}[/link]")
                print(
                    f"[bold green reverse]PUBLISHED:[/bold green reverse]{published}")

                # print first 250 characters of the summary and add ... if summary is longer than 250 characters
                summary = remove_html_tags(entry.summary)
                if len(summary) > 250:
                    summary = f"{summary[:250]}..."
                print(
                    f"[bold violet reverse]SUMMARY:[/bold violet reverse][dim]{summary}[/dim]")

                print("---------------------------------------------------")


# add_feed(url="https://www.reddit.com/r/Python/.rss")
# add_feed(url="https://pitchfork.com/rss/reviews/best/albums/")
# add_feed(url="https://www.tor.com/series/reading-the-wheel-of-time/feed/")
# add_feed(url="https://www.buzzfeed.com/in/index.xml")
# add_feed(url="https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml")
# get_all_feeds()
# remove_feed()

# check_feed_for_new_content(title="wheel of time")
