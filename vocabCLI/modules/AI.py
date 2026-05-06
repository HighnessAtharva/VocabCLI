"""AI module for VocabCLI 2026.

Central abstraction layer for all AI-powered features.  Supports:
- OpenAI (``gpt-4o`` / ``gpt-4o-mini``) via the modern ``openai>=1.0`` client.
- Ollama (local LLMs: Llama 3, Mistral, Phi-3, …) via the OpenAI-compatible
  REST endpoint at ``http://localhost:11434/v1``.

API-key lookup order:
1. ``OPENAI_API_KEY`` environment variable  (standard)
2. ``OPENAI`` environment variable          (legacy compat)
3. ``~/.vocabcli/config.toml``              (user config file)

Usage example::

    from vocabCLI.modules.AI import get_ai_client, stream_response

    client, model = get_ai_client()
    stream_response(client, model, "Explain the word 'ephemeral'")
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterator, Optional

from rich import print
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

_CONFIG_PATH = Path.home() / ".vocabcli" / "config.toml"

# ──────────────────────────────────────────────────────────────────────────────
# Configuration helpers
# ──────────────────────────────────────────────────────────────────────────────


def _read_config() -> dict:
    """Read ``~/.vocabcli/config.toml`` and return it as a dict.

    Returns an empty dict when the file does not exist or ``tomllib`` is
    unavailable.

    Returns:
        dict: Parsed configuration values.
    """
    try:
        import tomllib  # stdlib ≥ 3.11
    except ImportError:
        try:
            import tomli as tomllib  # noqa: F401  type: ignore[no-redef]
        except ImportError:
            return {}

    if not _CONFIG_PATH.exists():
        return {}
    try:
        with open(_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def _cfg(section: str, key: str, default: Optional[str] = None) -> Optional[str]:
    """Return a single value from the config file.

    Args:
        section (str): TOML table name (e.g. ``"ai"``).
        key (str): Key within the table.
        default (str, optional): Value to return when the key is absent.

    Returns:
        str | None: The configured value or *default*.
    """
    cfg = _read_config()
    return cfg.get(section, {}).get(key, default)


# ──────────────────────────────────────────────────────────────────────────────
# Client factory
# ──────────────────────────────────────────────────────────────────────────────


def get_ai_client(provider: Optional[str] = None) -> tuple:
    """Return an ``(openai.OpenAI, model_name)`` tuple.

    Resolves the provider and model from (in order of precedence):
    1. The *provider* argument (``"openai"`` or ``"ollama"``)
    2. ``~/.vocabcli/config.toml`` ``[ai]`` section
    3. Defaults (OpenAI + ``gpt-4o-mini``)

    For **Ollama**, uses the OpenAI-compatible endpoint on localhost:11434 so
    the same code path works for both providers.

    Args:
        provider (str, optional): Override the AI provider.
            One of ``"openai"`` or ``"ollama"``.

    Returns:
        tuple[openai.OpenAI, str]: ``(client, model_name)`` ready to use.

    Raises:
        SystemExit: When ``openai`` is not installed.
    """
    try:
        from openai import OpenAI
    except ImportError:
        print(
            Panel(
                title="[b reverse red]  Missing Dependency  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable=(
                    "The [bold cyan]openai[/bold cyan] package is not installed.\n"
                    "Install it with: [bold white]pip install \"vocabcli[ai]\"[/bold white]"
                ),
            )
        )
        sys.exit(1)

    resolved_provider = (
        provider
        or _cfg("ai", "provider")
        or "openai"
    ).lower()

    if resolved_provider == "ollama":
        base_url = _cfg("ai", "ollama_base_url") or "http://localhost:11434/v1"
        model = _cfg("ai", "model") or "llama3.2"
        client = OpenAI(api_key="ollama", base_url=base_url)
        return client, model

    # Default: OpenAI
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("OPENAI")
        or _cfg("ai", "api_key")
    )
    if not api_key:
        print(
            Panel(
                title="[b reverse yellow]  AI Not Configured  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=(
                    "No OpenAI API key found.\n\n"
                    "Run [bold white]vocab setup[/bold white] to configure AI features, "
                    "or set the [bold white]OPENAI_API_KEY[/bold white] environment variable.\n\n"
                    "🆓 Get a free key at [bold cyan]https://platform.openai.com/api-keys[/bold cyan]"
                ),
            )
        )
        sys.exit(1)

    model = _cfg("ai", "model") or "gpt-4o-mini"
    client = OpenAI(api_key=api_key)
    return client, model


# ──────────────────────────────────────────────────────────────────────────────
# Streaming helpers
# ──────────────────────────────────────────────────────────────────────────────


def stream_to_panel(
    client,
    model: str,
    prompt: str,
    title: str = "✨ AI Insight",
) -> str:
    """Stream a chat completion and render it in a Rich Live panel.

    The response streams character-by-character into a ``Live`` panel so the
    user sees output incrementally (like ChatGPT).

    Args:
        client: An ``openai.OpenAI`` client instance.
        model (str): Model name (e.g. ``"gpt-4o-mini"``).
        prompt (str): The user prompt to send.
        title (str): Title shown on the Rich panel.

    Returns:
        str: The complete response text.
    """
    full_text = ""
    with Live(
        Panel("", title=f"[bold green]{title}[/bold green]", padding=(1, 2)),
        refresh_per_second=15,
    ) as live:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full_text += delta
            live.update(
                Panel(
                    Markdown(full_text),
                    title=f"[bold green]{title}[/bold green]",
                    padding=(1, 2),
                )
            )
    return full_text


def simple_completion(client, model: str, prompt: str) -> str:
    """Return a non-streaming completion string.

    Args:
        client: An ``openai.OpenAI`` client instance.
        model (str): Model name.
        prompt (str): The user prompt.

    Returns:
        str: The response content.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


# ──────────────────────────────────────────────────────────────────────────────
# AI cache (SQLite)
# ──────────────────────────────────────────────────────────────────────────────


def _get_cached(word: str, cache_type: str) -> Optional[str]:
    """Retrieve a cached AI response from the database.

    Args:
        word (str): The vocabulary word.
        cache_type (str): The type of AI content (e.g. ``"mnemonic"``).

    Returns:
        str | None: Cached content, or ``None`` if not found.
    """
    from .Database import createConnection
    conn = createConnection()
    c = conn.cursor()
    c.execute(
        "SELECT content FROM ai_cache WHERE word=? AND type=?",
        (word.lower(), cache_type),
    )
    row = c.fetchone()
    return row[0] if row else None


def _save_to_cache(word: str, cache_type: str, content: str, model: str = "") -> None:
    """Save an AI response to the cache table.

    Args:
        word (str): The vocabulary word.
        cache_type (str): The type of AI content.
        content (str): The AI-generated text.
        model (str): The model that produced the content.
    """
    from datetime import datetime
    from .Database import createConnection
    conn = createConnection()
    c = conn.cursor()
    c.execute(
        """INSERT OR REPLACE INTO ai_cache (word, type, content, model, datetime)
           VALUES (?, ?, ?, ?, ?)""",
        (word.lower(), cache_type, content, model, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()


# ──────────────────────────────────────────────────────────────────────────────
# Core AI feature functions
# ──────────────────────────────────────────────────────────────────────────────


def ai_explain(word: str, provider: Optional[str] = None) -> None:
    """Stream a deep AI explanation of a vocabulary word.

    Covers etymology, root meaning, historical context, register
    (formal/informal/archaic), common mistakes, and when to use vs. avoid.
    Caches the result so repeated calls are instant.

    Args:
        word (str): The word to explain.
        provider (str, optional): AI provider override (``"openai"`` or ``"ollama"``).
    """
    cached = _get_cached(word, "explain")
    if cached:
        print(
            Panel(
                Markdown(cached),
                title=f"[bold green]✨ AI Explanation — {word.upper()}[/bold green]",
                padding=(1, 2),
            )
        )
        return

    client, model = get_ai_client(provider)
    prompt = (
        f"Give a rich, educator-quality explanation of the word **{word}**.\n\n"
        "Cover ALL of the following in your response:\n"
        "1. **Etymology & roots** – where does this word come from?\n"
        "2. **Core meaning** – plain-English definition\n"
        "3. **Register** – is it formal, informal, literary, or archaic?\n"
        "4. **When to USE it** – ideal contexts with a brief example\n"
        "5. **When NOT to use it** – common misapplications or confusable words\n"
        "6. **Memory tip** – a vivid association to remember it\n\n"
        "Be concise but thorough. Use markdown formatting."
    )
    result = stream_to_panel(client, model, prompt, title=f"✨ AI Explanation — {word.upper()}")
    _save_to_cache(word, "explain", result, model)


def ai_mnemonic(word: str, provider: Optional[str] = None) -> str:
    """Generate (or retrieve cached) a mnemonic for a vocabulary word.

    Args:
        word (str): The word to generate a mnemonic for.
        provider (str, optional): AI provider override.

    Returns:
        str: The mnemonic text.
    """
    cached = _get_cached(word, "mnemonic")
    if cached:
        print(
            Panel(
                cached,
                title=f"[bold magenta]🧠 Mnemonic — {word.upper()}[/bold magenta]",
                padding=(1, 2),
            )
        )
        return cached

    client, model = get_ai_client(provider)
    prompt = (
        f"Create ONE vivid, memorable mnemonic to help someone remember the meaning "
        f"of the word **{word}**.\n\n"
        "Rules:\n"
        "- Keep it to 1–3 sentences\n"
        "- Use wordplay, imagery, or a memorable story hook\n"
        "- Start with 'Think of…' or 'Remember…'\n"
        "- The word itself should appear in ALL CAPS once\n\n"
        "Example for 'ephemeral': Think of an EP record — EPHEMERAL things last about "
        "as long as it takes to play one side."
    )
    result = simple_completion(client, model, prompt)
    _save_to_cache(word, "mnemonic", result, model)
    print(
        Panel(
            result,
            title=f"[bold magenta]🧠 Mnemonic — {word.upper()}[/bold magenta]",
            padding=(1, 2),
        )
    )
    return result


def ai_story(provider: Optional[str] = None) -> None:
    """Generate a short story using words from the learning list.

    Reads the user's current ``learning`` word list from the database and asks
    the AI to weave all of them naturally into a 150–200 word paragraph.

    Args:
        provider (str, optional): AI provider override.
    """
    from .Database import createConnection
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT word FROM words WHERE learning=1")
    rows = c.fetchall()
    if not rows:
        print(
            Panel(
                title="[b reverse yellow]  No Learning Words  [/b reverse yellow]",
                title_align="center",
                padding=(1, 1),
                renderable=(
                    "Your learning list is empty. Add words with "
                    "[bold white]vocab learn <word>[/bold white] first."
                ),
            )
        )
        return

    words = [r[0] for r in rows]
    client, model = get_ai_client(provider)
    words_str = ", ".join(f"**{w}**" for w in words)
    prompt = (
        f"Write a short, engaging story (150–200 words) that naturally and correctly "
        f"uses ALL of the following vocabulary words: {words_str}.\n\n"
        "Requirements:\n"
        "- Each listed word must appear at least once, bolded\n"
        "- The story should feel natural, not forced\n"
        "- Genre: your choice (fiction, fable, micro-essay, etc.)\n"
        "- After the story, list each word with its one-line definition used in context"
    )
    stream_to_panel(client, model, prompt, title="📖 Vocabulary Story")


def ai_sentences(word: str, provider: Optional[str] = None) -> None:
    """Generate three contextually diverse example sentences for a word.

    Produces one formal, one casual, and one literary sentence to complement
    the dictionary API's single static example.

    Args:
        word (str): The word to generate sentences for.
        provider (str, optional): AI provider override.
    """
    cached = _get_cached(word, "sentences")
    if cached:
        print(
            Panel(
                Markdown(cached),
                title=f"[bold cyan]📝 Example Sentences — {word.upper()}[/bold cyan]",
                padding=(1, 2),
            )
        )
        return

    client, model = get_ai_client(provider)
    prompt = (
        f"Generate exactly 3 example sentences for the word **{word}**:\n\n"
        "1. **Formal** – academic or professional register\n"
        "2. **Casual** – everyday conversation\n"
        "3. **Literary** – evocative, poetic, or narrative style\n\n"
        "Bold the word **{word}** each time it appears. Keep each sentence under 25 words."
    )
    result = stream_to_panel(client, model, prompt, title=f"📝 Example Sentences — {word.upper()}")
    _save_to_cache(word, "sentences", result, model)


def ai_suggest(provider: Optional[str] = None) -> None:
    """Suggest the next 10 words to learn based on the user's vocabulary history.

    Analyses the words the user has looked up and recommends complementary words
    that fit their apparent learning focus (literary, academic, conversational, …).

    Args:
        provider (str, optional): AI provider override.
    """
    from .Database import createConnection
    conn = createConnection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT word FROM words ORDER BY datetime DESC LIMIT 30")
    rows = c.fetchall()
    if not rows:
        print(Panel("Look up some words first with [bold]vocab define[/bold] to get personalised suggestions."))
        return

    recent_words = [r[0] for r in rows]
    client, model = get_ai_client(provider)
    words_str = ", ".join(recent_words)
    prompt = (
        f"A vocabulary learner's recent word lookups include: {words_str}\n\n"
        "Based on this list:\n"
        "1. Identify the apparent vocabulary focus (e.g., literary, academic, conversational)\n"
        "2. Recommend exactly **10 new words** they should learn next, chosen to:\n"
        "   - Complement their existing vocabulary level\n"
        "   - Fill obvious gaps in their word knowledge\n"
        "   - Be genuinely useful in real-world usage\n\n"
        "For each recommended word provide: the word, its part of speech, "
        "and a one-sentence reason why it belongs at this learner's level.\n\n"
        "Format as a numbered list."
    )
    stream_to_panel(client, model, prompt, title="💡 Personalised Word Suggestions")


def ai_quiz(word_list: Optional[list] = None, provider: Optional[str] = None) -> None:
    """Run an AI-generated vocabulary quiz.

    Generates diverse question types (fill-in-the-blank, analogies, usage in
    context, find-the-odd-one-out) that are significantly harder and more
    educational than the classic 4-choice definition quiz.

    Args:
        word_list (list, optional): Words to quiz on. Defaults to learning list.
        provider (str, optional): AI provider override.
    """
    from .Database import createConnection
    conn = createConnection()
    c = conn.cursor()

    if word_list:
        words = word_list
    else:
        c.execute("SELECT DISTINCT word FROM words WHERE learning=1 ORDER BY RANDOM() LIMIT 10")
        rows = c.fetchall()
        if not rows:
            print(Panel("Add words to your learning list first with [bold]vocab learn <word>[/bold]."))
            return
        words = [r[0] for r in rows]

    client, model = get_ai_client(provider)
    words_str = ", ".join(f"**{w}**" for w in words)
    prompt = (
        f"Create a challenging vocabulary quiz using these words: {words_str}\n\n"
        "Include a mix of these question types (use each at least once):\n"
        "- Fill-in-the-blank (provide a sentence with the word removed)\n"
        "- Analogy (e.g. 'ephemeral : permanent :: __ : ___')\n"
        "- Usage in context (is this sentence using the word correctly? Yes/No + explanation)\n"
        "- Find the odd one out (which word doesn't belong? Why?)\n\n"
        "Format clearly with question numbers. Show the answer after each question "
        "in a collapsible spoiler: >! answer !<"
    )
    stream_to_panel(client, model, prompt, title="❓ AI Vocabulary Quiz")


def ai_chat(provider: Optional[str] = None) -> None:
    """Launch an interactive AI vocabulary tutor chat session.

    Maintains conversation context within the session.  The user can ask
    anything vocabulary-related: word differences, etymology, usage, etc.
    Type ``exit`` or ``quit`` to end the session.

    Args:
        provider (str, optional): AI provider override.
    """
    client, model = get_ai_client(provider)
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert vocabulary tutor and linguist. Help the user "
                "understand words deeply — their meanings, etymology, usage, nuances, "
                "and common mistakes. Be engaging, educational, and concise. "
                "Use examples liberally."
            ),
        }
    ]

    print(
        Panel(
            "[bold green]🎓 AI Vocabulary Tutor[/bold green]\n\n"
            "Ask me anything about words — definitions, differences, etymology, usage…\n"
            "Type [bold red]exit[/bold red] or [bold red]quit[/bold red] to end the session.",
            title="[reverse]Vocabulary Chat[/reverse]",
            title_align="center",
            padding=(1, 2),
        )
    )

    while True:
        try:
            user_input = input("\n[You]: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in ("exit", "quit", "q", "bye"):
            print(Panel("👋 Chat session ended. Keep building that vocabulary!", padding=(1, 2)))
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        full_response = ""
        with Live(
            Panel("", title="[bold green]🤖 Tutor[/bold green]", padding=(1, 2)),
            refresh_per_second=15,
        ) as live:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                live.update(
                    Panel(
                        Markdown(full_response),
                        title="[bold green]🤖 Tutor[/bold green]",
                        padding=(1, 2),
                    )
                )

        messages.append({"role": "assistant", "content": full_response})


def ai_paraphrase(text: str, provider: Optional[str] = None) -> None:
    """Paraphrase text using the AI (replaces the heavy transformer approach).

    Replaces the original ``torch + transformers`` paraphrase function with a
    lightweight OpenAI API call that starts in milliseconds rather than
    loading a 500 MB model.

    Args:
        text (str): Text to paraphrase.
        provider (str, optional): AI provider override.
    """
    client, model = get_ai_client(provider)
    prompt = (
        f"Paraphrase the following text. Keep the meaning identical but use different "
        f"words and sentence structure. Provide 2 alternatives:\n\n{text}"
    )
    stream_to_panel(client, model, prompt, title="🔄 Paraphrase")
