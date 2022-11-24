from rich import print

class WordNeverSearchedException(Exception):
    """raised when a word is never searched but user attempts to perform some operation on it."""
    word=None
    def __init__(self, word):
        self.word=word
        print(f"The word [bold red]{self.word}[/bold red] was never tracked before. Lookup using 'define' command first.")
        
class AudioUnavailableException(Exception):
    """raised when the audio is not available for the word."""
    def __init__(self):
        print("[bold red]Audio Unavailable[/bold red]")
    
class NothingToDeleteException(Exception):
    """raised when the user attempts to delete a word which is not present in the database."""
    def __init__(self):
        print("[bold red]Nothing to delete[/bold red]")

class NoDataFoundException(Exception):
    """raised when the user attempts to export data but there is no data to export."""
    def __init__(self):
        print("[bold red]No words to export. Lookup using 'define' command first.[/bold red]")