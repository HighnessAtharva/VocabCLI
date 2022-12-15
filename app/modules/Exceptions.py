from rich import print
from rich.panel import Panel

class WordNeverSearchedException(Exception):
    """raised when a word is never searched but user attempts to perform some operation on it."""
    word=None
    def __init__(self, word):
        self.word=word
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"The word [bold red]{self.word}[/bold red] was never tracked before. Add some words in your list using 'define' command first. 🔎")
        ) 
        
class AudioUnavailableException(Exception):
    """raised when the audio is not available for the word."""
    def __init__(self):
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]Audio Unavailable[/bold red] ❌")
        ) 
        

class NoDataFoundException(Exception):
    """raised when the user attempts to export data but there is no data to export."""
    def __init__(self):
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]No words to export ❌. Add some words in your list using 'define' command ➕. [/bold red]")
        ) 

class NoWordsInDB(Exception):
    """raised when the user attempts to perform some operation on a word which is not present in the database."""
    word=None
    def __init__(self):
        self.word=word
        print(Panel.fit(
                title="[b reverse red]  Error!  [/b reverse red]",
                title_align="center",
                padding=(1, 1),
                renderable="There are no words in any of your lists. Add some words in your list using 'define' command first. 🔎",
            )
        )
        
class NoWordsInLearningList(Exception):
    """raised when the user attempts to start a learning session but there are no words in the list."""
    def __init__(self):
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]No words in your learning list. Add some words in your list using 'learn [word]' command first. 🔎[/bold red]")
        )

class NoWordsInMasteredList(Exception):
    """raised when the user attempts to start a learning session but there are no words in the list."""
    def __init__(self):
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]No words in your mastered list. Add some words in your list using 'master [word]' command first. 🔎[/bold red]")
        )
        
class NoWordsInFavoriteList(Exception):
        """raised when the user attempts to start a learning session but there are no words in the list."""
        def __init__(self):
            print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                    title_align="center",
                    padding=(1, 1),
                    renderable="[bold red]No words in your favorite list. Add some words in your list using 'favorite [word]' command first. 🔎[/bold red]")
            )
            

         
class NotEnoughWordsForQuizException(Exception):
    """raised when the user attempts to start a quiz but there are not enough words in the list."""
    def __init__(self):
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable="[bold red]Not enough words to start a quiz. Add some words in your list using 'define' command first. 🔎[/bold red]")
        )
        
class NoSuchCollectionException(Exception):
    """raised when the user attempts to perform some operation on a collection which is not present in the list."""
    collection=None
    def __init__(self, collection):
        self.collection=collection
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"The collection [bold red]{self.collection}[/bold red] is not present in the list. See available collections using the 'list --collections' command. 📚")
        )    
        
class NoSuchTagException(Exception):
    """raised when the user attempts to perform some operation on a tag which is not present in the list."""
    tag=None
    def __init__(self, tag):
        self.tag=tag
        print(Panel.fit(title="[b reverse red]  Error!  [/b reverse red]", 
                title_align="center",
                padding=(1, 1),
                renderable=f"The tag [bold red]{self.tag}[/bold red] is not present in the list. Add some tags in your list using 'tag' command first. To see currently added tags use the 'list --tags' command🔖")
        )