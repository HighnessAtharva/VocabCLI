"""Configuration management for VocabCLI.

Reads and writes ``~/.vocabcli/config.toml``.

Usage::

    from vocabCLI.modules.Config import get_config, set_config, show_config

    api_key = get_config("ai", "api_key")
    set_config("ai", "provider", "ollama")
    show_config()
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

CONFIG_DIR = Path.home() / ".vocabcli"
CONFIG_PATH = CONFIG_DIR / "config.toml"

_DEFAULT_CONFIG = """\
# VocabCLI Configuration
# Edit this file or use: vocab config set <section.key> <value>
# Docs: https://vocabcli.github.io/docs/configuration

[ai]
# provider = "openai"     # "openai" or "ollama"
# model    = "gpt-4o-mini"
# api_key  = ""           # or set OPENAI_API_KEY env var
# ollama_base_url = "http://localhost:11434/v1"

[display]
# style = "rich"          # "rich" or "minimal"

[paths]
# db_path = ""            # override default: ~/.vocabcli/VocabularyBuilder.db

[features]
# ai_enabled   = true
# srs_enabled  = true
# streak_enabled = true
"""


def _ensure_config_dir() -> None:
    """Create the ``~/.vocabcli/`` directory if it does not exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_raw() -> str:
    """Return the raw TOML text of the config file, creating it if needed.

    Returns:
        str: Raw TOML text.
    """
    _ensure_config_dir()
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(_DEFAULT_CONFIG, encoding="utf-8")
    return CONFIG_PATH.read_text(encoding="utf-8")


def _parse() -> dict:
    """Parse and return the config file as a nested dict.

    Returns:
        dict: Parsed configuration.
    """
    try:
        import tomllib  # stdlib ≥ 3.11
    except ImportError:
        try:
            import tomli as tomllib  # noqa: F401  type: ignore[no-redef]
        except ImportError:
            return {}

    raw = _load_raw()
    try:
        return tomllib.loads(raw)
    except Exception:
        return {}


def get_config(section: str, key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a configuration value.

    Args:
        section (str): TOML table name (e.g. ``"ai"``).
        key (str): Key within the table.
        default (str, optional): Fallback value.

    Returns:
        str | None: The configured value, or *default*.
    """
    return _parse().get(section, {}).get(key, default)


def set_config(section: str, key: str, value: str) -> None:
    """Write a key-value pair to the config file.

    Uses simple string manipulation to preserve comments and ordering.

    Args:
        section (str): TOML table name.
        key (str): Key within the table.
        value (str): New value (written as a TOML string).
    """
    _ensure_config_dir()
    raw = _load_raw()
    lines = raw.splitlines(keepends=True)
    in_section = False
    key_found = False
    new_line = f'{key} = "{value}"\n'

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f"[{section}]":
            in_section = True
            continue
        if in_section:
            if stripped.startswith("[") and stripped.endswith("]"):
                # We've moved to the next section without finding the key
                if not key_found:
                    lines.insert(i, new_line)
                    key_found = True
                break
            # Match both active and commented-out key
            bare = stripped.lstrip("# ")
            if bare.startswith(f"{key} =") or bare.startswith(f"{key}="):
                lines[i] = new_line
                key_found = True
                break

    if not key_found:
        # Append section + key if section not present
        if f"[{section}]" not in raw:
            lines.append(f"\n[{section}]\n{new_line}")
        else:
            lines.append(new_line)

    CONFIG_PATH.write_text("".join(lines), encoding="utf-8")


def show_config() -> None:
    """Display the current configuration in a Rich table."""
    cfg = _parse()

    print(
        Panel(
            f"[bold]Config file:[/bold] {CONFIG_PATH}",
            title="[reverse]VocabCLI Configuration[/reverse]",
            title_align="center",
            padding=(1, 1),
        )
    )

    if not cfg:
        print(Panel("No configuration found. Run [bold]vocab setup[/bold] to get started."))
        return

    table = Table(show_header=True, header_style="bold gold3", expand=True)
    table.add_column("Section", style="cyan", width=12)
    table.add_column("Key", style="blue", width=20)
    table.add_column("Value", style="green")

    for section, pairs in cfg.items():
        if isinstance(pairs, dict):
            for k, v in pairs.items():
                table.add_row(f"[{section}]", k, str(v))
            table.add_section()

    print(table)
