import contextlib
from datetime import datetime, timedelta
from pathlib import Path
from sqlite3 import *
from typing import *

import feedparser
import typer
from bs4 import BeautifulSoup
from Database import createConnection, createTables
from Exceptions import *
from rich import box, print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table


def add_feed(url: str) -> None:
    """
    Add the feed to the database

    1. Feed parser is used to parse the feed
    2. If the feed is not found, print error message
    3. Check if the feed exists in the database
    4. If it does not exist, add it to the database
    5. If it does exist, print error message

    Args:
        url (str): The URL of the feed
    """

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Adding Feed", total=None)
        # ----------------- Spinner -----------------#
        try:
            # parse the feed
            feed = feedparser.parse(url)

            # if URL is not a feed URL or does not return a 200 status code, print error message
            if feed.status != 200 or feed.bozo:
                print(
                    Panel(
                        title="[b reverse red]  Error!  [/b reverse red]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="Feed not found ❌",
                    )
                )
                return
        except Exception as e:
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="Feed not found ❌",
                )
            )
            return

        conn = createConnection()
        c = conn.cursor()

        # check if feed exists in the database
        c.execute("SELECT * from rss where link=?", (url,))
        if c.fetchone():
            print(
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable=" Feed already exists ✅",
                )
            )
            return

        # add feed to database if it does not exist
        # NOTE: feed.feed.link is not the same as url, you want to store the RSS feed URL, not the website URL
        c.execute(
            "INSERT INTO rss (title, link, description, datetime) VALUES (?, ?, ?, ?)",
            (
                feed.feed.title,
                url,
                feed.feed.description,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            ),
        )
        conn.commit()

        print(
            Panel(
                title="[b reverse]  Feed added successfully ✅  [/b reverse]",
                renderable=f"Title:  {feed.feed.title}\n\nLink:  {feed.feed.link}\n\nSummary: {feed.feed.description}",
            )
        )


def get_all_feeds() -> None:
    """
    Get the feed details from the database

    1. Get all feeds from the database
    2. If no feeds exist, print error message
    3. Print the feeds in a table
    """

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
        transient=True,
    ) as progress:
        progress.add_task(description="Getting your feeds", total=None)
        # ----------------- Spinner -----------------#

        conn = createConnection()
        c = conn.cursor()

        try:
            # get all feeds
            c.execute("SELECT * from rss")
            rows = c.fetchall()

            # if no feeds exist, print error message
            if not rows:
                raise NoRSSFeedsException()

            # ----------------- Table -----------------#

            table = Table(
                show_header=True,
                header_style="bold gold3",
                border_style="white",
                title="📰 YOUR FEEDS ",
                title_style="bold magenta",
                title_justify="center",
                box=box.ROUNDED,
            )
            table.add_column("🌐 Title", width=30)
            table.add_column("🔗 Link", width=30, style="blue")
            table.add_column("📃 Summary", width=60, style="bright_green italic")
            table.add_column("📅 Date added", width=18, style="magenta")

            for row in rows:
                # do not display the RSS feed URL, display the website URL instead
                link = feedparser.parse(row[1]).feed.link
                table.add_row(
                    f"[b u cyan]{row[0]}[/b u cyan]",
                    link,
                    row[2],
                    datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M").strftime(
                        "%d %b '%y | %H:%M"
                    ),
                )
                table.add_row("\n", "\n", "\n", "\n")
                table.add_section()
            print(table)

            # ----------------- Table -----------------#

        except NoRSSFeedsException as e:
            print(e)


def remove_feed() -> None:
    """
    Remove the feed from the database

    1. Get all feeds from the database
    2. If no feeds exist, print error message
    3. Print the feeds in a table
    4. Ask the user to select the feed to remove
    5. Remove the feed from the database
    """

    conn = createConnection()
    c = conn.cursor()

    # check if feed exists in the database
    c.execute("SELECT * from rss")
    rows = c.fetchall()
    if not rows:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="Feed does not exist ❌",
            )
        )
        return

    # print the table using rich
    table = Table(
        show_header=True,
        header_style="bold gold3",
        border_style="white",
        title="📰 YOUR FEEDS ",
        title_style="bold magenta",
        title_justify="center",
        box=box.ROUNDED,
    )
    table.add_column("🔢 Index", width=10)
    table.add_column("🌐 Title", width=30)
    table.add_column("🔗 Link", width=30, style="blue")
    table.add_column("📃 Summary", width=60, style="bright_green italic")
    table.add_column("📅 Date added", width=18, style="magenta")

    for idx, row in enumerate(rows, start=1):
        table.add_row(
            f"[b u cyan]{idx}[/b u cyan]",
            f"[b u cyan]{row[0]}[/b u cyan]",
            row[1],
            row[2],
            datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M").strftime(
                "%d %b '%y | %H:%M"
            ),
        )
        table.add_row("\n", "\n", "\n", "\n", "\n")
        table.add_section()
    print(table)

    print(Panel("Enter the index of the feed you want to remove!"))
    try:
        index = int(input("Index: "))
    except ValueError:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="Index should be a number 🔢",
            )
        )
        return
    if index > len(rows):
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="Invalid index, out of range ❌",
            )
        )
        return

    feed_name = rows[index - 1][0]
    # remove feed from database
    c.execute("DELETE FROM rss WHERE title=?", (feed_name,))
    conn.commit()
    print(
        Panel(
            title="[b reverse green]  Delete Successful!  [/b reverse green]",
            renderable=f"Feed {feed_name} [bold red]deleted[/bold red] successfully ✅",
        )
    )


def remove_html_tags(html: str) -> str:
    """
    Remove html tags from a string

    Args:
        html (str): HTML string
    """

    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["style", "script"]):
        # Remove tags
        data.decompose()
    return " ".join(soup.stripped_strings)


def check_feed_for_new_content(title: str) -> None:
    """
    Parse the feed and check for new content

    1. Check if the feed exists in the database
    2. If the feed does not exist, print error message
    3. If the feed exists, parse the feed and check for new content
    4. If new content is found, print the new content
    5. If no new content is found, print error message

    Args:
        title (str): Title of the feed
    """

    # ----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="clock", style="bold violet"),
        TextColumn(
            "[progress.description]{task.description}",
            justify="left",
            style="bold cyan",
        ),
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
                Panel(
                    title="[b reverse red]  Error!  [/b reverse red]",
                    title_align="center",
                    padding=(1, 1),
                    renderable="This feed is [bold red]not added to your list[/bold red]. Use [bold blue]'rss' command[/bold blue] to add a feed. ➕",
                )
            )
            return

        for row in rows:
            feed = feedparser.parse(row[1])

            # ----------------- Table -----------------#

            table = Table(
                show_header=True,
                header_style="bold gold3",
                border_style="white",
                title=f"📰 ARTICLES FROM {row[0]}",
                title_style="bold magenta",
                title_justify="center",
                box=box.ROUNDED,
            )
            table.add_column(
                "🌐 Title", width=40, justify="center", style="bright_green"
            )
            table.add_column("📅 Published On", width=20, style="blue")
            table.add_column("📄 Article Summary", width=85, style="white italic")

            # sorting by reverse chronological order
            for entry in sorted(feed.entries, key=lambda x: x.published):
                published = entry.published_parsed

                # convert 8 tuple to datetime object
                published = datetime.datetime(*published[:6])
                published = published.strftime("%d %b '%y | %H:%M")

                # print first 250 characters of the summary and add ... if summary is longer than 250 characters
                summary = remove_html_tags(entry.summary)
                if len(summary) > 250:
                    summary = f"{summary[:250]}..."

                # if summary is empty, add a default message
                if summary == "":
                    summary = "No summary available 📪"

                table.add_row(
                    f"[link={str(entry.link)}]{remove_html_tags(entry.title)}[/link]",
                    f"{published}",
                    f"{summary}",
                )
                table.add_section()

            print(table)

            # ----------------- Table -----------------#
