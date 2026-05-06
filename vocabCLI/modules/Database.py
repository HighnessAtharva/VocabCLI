import calendar
import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from sqlite3 import Error

import requests
from requests import exceptions
from rich import print
from rich.panel import Panel

# from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress import track


def _get_db_path() -> str:
    """Return the path to the SQLite database.

    The path can be overridden via the ``VOCABCLI_DB_PATH`` environment variable
    (useful in tests).  Otherwise the database lives in ``~/.vocabcli/``.
    In both cases, the parent directory is created if it does not exist.

    Returns:
        str: Absolute path to the database file.
    """
    if env_path := os.getenv("VOCABCLI_DB_PATH"):
        Path(env_path).parent.mkdir(parents=True, exist_ok=True)
        return env_path
    db_dir = Path.home() / ".vocabcli"
    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / "VocabularyBuilder.db")


# no tests for this function as it is not called anywhere in the command directly
def createConnection():
    """
    Creates a database connection to the VocabularyBuilder SQLite database.

    The database is stored in ``~/.vocabcli/VocabularyBuilder.db`` so that it
    persists across working-directory changes and is user-scoped.  The path can
    be overridden via the ``VOCABCLI_DB_PATH`` environment variable (used by the
    test suite).

    Returns:
        sqlite3.Connection | None: Connection object, or None on error.
    """
    conn = None
    try:
        conn = sqlite3.connect(_get_db_path())
    except Error as e:
        print(e)
    return conn


# no tests for this function as it is not called anywhere in the command directly
def createTables(conn: sqlite3.Connection) -> None:
    """
    Creates the application tables in the database if they do not exist.

    Tables created:
        - ``words``        – vocabulary entries with SRS scheduling columns
        - ``cache_words``  – API response cache to reduce network calls
        - ``collections``  – curated word-to-domain mappings
        - ``quiz_history`` – history of quiz sessions
        - ``quotes``       – user-saved quotes
        - ``rss``          – tracked RSS feeds
        - ``ai_cache``     – cached AI-generated insights (mnemonics, explanations)
        - ``streaks``      – daily activity log for streak tracking

    Args:
        conn (sqlite3.Connection): Active database connection.
    """

    words = """CREATE TABLE IF NOT EXISTS "words" (
	"word"	TEXT,
	"datetime"	timestamp NOT NULL UNIQUE,
	"tag"	TEXT,
	"mastered"	INTEGER NOT NULL DEFAULT 0,
	"learning"	INTEGER NOT NULL DEFAULT 0,
	"favorite"	INTEGER NOT NULL DEFAULT 0,
	"ease_factor"	REAL NOT NULL DEFAULT 2.5,
	"interval_days"	INTEGER NOT NULL DEFAULT 1,
	"next_review_date"	TEXT,
	"review_count"	INTEGER NOT NULL DEFAULT 0
);
    """

    cache_words = """CREATE TABLE IF NOT EXISTS "cache_words" (
	"word"	TEXT NOT NULL UNIQUE,
    "api_response" json NOT NULL
);
    """

    collections = """CREATE TABLE IF NOT EXISTS "collections" (
            "word"	TEXT NOT NULL,
            "collection" TEXT NOT NULL
            );
        """

    quiz_history = """CREATE TABLE IF NOT EXISTS "quiz_history" (
            "type" TEXT NOT NULL,
            "datetime" timestamp NOT NULL UNIQUE,
            "question_count" INTEGER NOT NULL,
            "points" INTEGER NOT NULL,
            "duration" INTEGER NOT NULL
            );
        """

    quotes = """ CREATE TABLE IF NOT EXISTS "quotes" (
            "quote" TEXT NOT NULL UNIQUE,
            "author" TEXT,
            "datetime" timestamp NOT NULL
            );
            """

    rss = """ CREATE TABLE IF NOT EXISTS "rss" (
            "title" TEXT NOT NULL,
            "link" TEXT NOT NULL UNIQUE,
            "description" TEXT,
            "datetime" timestamp NOT NULL
            );
            """

    ai_cache = """CREATE TABLE IF NOT EXISTS "ai_cache" (
            "word"      TEXT NOT NULL,
            "type"      TEXT NOT NULL,
            "content"   TEXT NOT NULL,
            "model"     TEXT,
            "datetime"  timestamp NOT NULL,
            PRIMARY KEY ("word", "type")
            );
            """

    streaks = """CREATE TABLE IF NOT EXISTS "streaks" (
            "date" TEXT NOT NULL UNIQUE,
            "word_count" INTEGER NOT NULL DEFAULT 0
            );
            """

    try:
        c = conn.cursor()
        c.executescript(
            words + cache_words + collections + quiz_history + quotes + rss + ai_cache + streaks
        )  # execute multiple statements
        # Migrate existing databases: add SRS columns if absent
        for col, definition in [
            ("ease_factor", "REAL NOT NULL DEFAULT 2.5"),
            ("interval_days", "INTEGER NOT NULL DEFAULT 1"),
            ("next_review_date", "TEXT"),
            ("review_count", "INTEGER NOT NULL DEFAULT 0"),
        ]:
            try:
                c.execute(f'ALTER TABLE words ADD COLUMN "{col}" {definition}')
                conn.commit()
            except Exception:
                pass  # column already exists
    except Exception as e:
        print(e)


# no tests for this function as it is not called anywhere in the command directly
def initializeDB() -> None:
    """Initializes the database, creating tables and running any pending migrations."""

    conn = createConnection()
    createTables(conn)


# NOTE: Use this command very sparingly. It is not recommended to use this command more than once a week due to possible API overuse
def refresh_cache() -> None:
    """Refreshes the API response cache for every tracked word.

    Fetches an up-to-date response from the dictionary API for every word
    stored in the ``cache_words`` table.  Runs concurrent requests using
    ``httpx.AsyncClient`` to avoid the previous sequential bottleneck.

    Skips gracefully when the cache is empty or the network is unavailable.
    """

    import asyncio

    import httpx

    conn = createConnection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM cache_words")
    if not c.fetchone()[0]:
        return
    c.execute("SELECT word FROM cache_words")
    rows = [r[0] for r in c.fetchall()]

    API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    async def _fetch_all(words: list[str]) -> dict[str, str]:
        results: dict[str, str] = {}
        async with httpx.AsyncClient(timeout=10) as client:
            tasks = {word: client.get(API_URL.format(word=word)) for word in words}
            for word, coro in tasks.items():
                try:
                    resp = await coro
                    if resp.status_code == 200:
                        results[word] = json.dumps(resp.json()[0])
                except Exception:
                    pass
        return results

    try:
        updated = asyncio.run(_fetch_all(rows))
    except Exception:
        print(
            Panel(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]Cache refresh failed. Check your internet connection.[/bold red] ❌",
            )
        )
        return

    for word, payload in track(updated.items(), description=" 🔃 Updating Cache "):
        c.execute(
            "UPDATE cache_words SET api_response=? WHERE word=?",
            (payload, word),
        )
    conn.commit()

    print(
        Panel(
            title="[b reverse green]  Success!  [/b reverse green]",
            title_align="center",
            padding=(1, 1),
            renderable=f"Cache refreshed for [bold green]{len(updated)}[/bold green] word(s). ✅",
        )
    )
