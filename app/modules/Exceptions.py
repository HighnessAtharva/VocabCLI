from rich import print
from rich.panel import Panel

class WordNeverSearchedException(Exception):
    """raised when a word is never searched but user attempts to perform some operation on it."""
    word=None
    def __init__(self, word):
        self.word=word
        print(Panel(f"The word [bold red]{self.word}[/bold red] was never tracked before. Add some words in your list using 'define' command first. 🔎"))
        
        
class AudioUnavailableException(Exception):
    """raised when the audio is not available for the word."""
    def __init__(self):
        print(Panel("[bold red]Audio Unavailable[/bold red] ❌"))
        

class NoDataFoundException(Exception):
    """raised when the user attempts to export data but there is no data to export."""
    def __init__(self):
        print(Panel("[bold red]No words to export ❌. Add some words in your list using 'define' command ➕. [/bold red]"))