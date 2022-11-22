from rich import print

class WordNeverSearchedException(Exception):
    """raised when a word is never searched but user attempts to perform some operation on it."""
    def __init__(self):
        print("[bold red] This word is never tracked before. use 'define' command first[/bold red]")
        
class AudioUnavailableException(Exception):
    """raised when the audio is not available for the word."""
    def __init__(self):
        print("[bold red]Audio Unavailable[/bold red]")
    
    