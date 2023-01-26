import os
from platform import platform, system

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from . import __app_name__, __version__


# no tests for this function as it is not called anywhere in the command directly
def get_terminal_width() -> int:
    """
    Gets the width of the terminal.

    Returns:
        int: width of the terminal.
    """
    try:
        width, _ = os.get_terminal_size()
    except OSError:
        width = 80

    if system().lower() == "windows":
        width -= 1

    return width


def print_banner(console) -> None:
    """
    Prints the banner of the application.

    Args:
        console (Console): Rich console object.
    """

    banner = """
             _    __                     __            __                       ____          _  __     __           
            | |  / /____   _____ ____ _ / /_   __  __ / /____ _ _____ __  __   / __ ) __  __ (_)/ /____/ /___   _____
            | | / // __ \ / ___// __ `// __ \ / / / // // __ `// ___// / / /  / __  |/ / / // // // __  // _ \ / ___/
            | |/ // /_/ // /__ / /_/ // /_/ // /_/ // // /_/ // /   / /_/ /  / /_/ // /_/ // // // /_/ //  __// /    
            |___/ \____/ \___/ \__,_//_.___/ \__,_//_/ \__,_//_/    \__, /  /_____/ \__,_//_//_/ \__,_/ \___//_/     
                                                                   /____/                                            
            """
    width = get_terminal_width()
    height = 10

    panel = Panel(
        Align(
            Text(banner, style="green"),
            vertical="middle",
            align="center",
        ),
        width=width,
        height=height,
        subtitle=f"[bold blue]v.{__version__} by Atharva & Anay[/bold blue]",
    )
    console.print(panel)
