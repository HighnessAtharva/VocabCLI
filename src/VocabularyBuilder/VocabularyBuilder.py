import typer
from rich import print

app = typer.Typer(
    name="Vocabulary Builder", 
    add_completion=False, 
    rich_markup_mode="rich",
    help=":book: [bold green]This is a dictionary and a vocabulary builder CLI.[/bold green]"
    )


"""
APP COMMANDS
"""

@app.command(rich_help_panel="Account")
def create(
    username: str=typer.Option(..., prompt=True, help="Set a username"),  
    password: str=typer.Option(..., prompt=True, confirmation_prompt=True,  hide_input=True, help="Set a Password")
    ):    
    
    """➕ [bold green]Create a user account[/bold green]"""
    
    print(f"[bold green]Created user: {username}[/bold green]")
    login(username, password)
    
    
@app.command(rich_help_panel="Account")
def delete( username: str=typer.Option(..., prompt=True, help="User to  deleted"),
            password: str=typer.Option(..., prompt=True, hide_input=True, help="Your Password")):
    
    """❌ [bold red]Delete a user account[/bold red]"""
    
    print(f"[bold red]Deleted user: {username}[/bold red]")


    
@app.command(rich_help_panel="Account")
def login(
    username: str=typer.Option(..., prompt=True, help="Your username"),  
    password: str=typer.Option(..., prompt=True, hide_input=True, help="Your Password")
    ):
    
    """🔑 [bold blue]Login to your account[/bold blue]"""
    
    print(f"[bold green]Logged in as: {username}[/bold green]");



"""
DICTIONARY COMMANDS
"""
@app.command(rich_help_panel="Dictionary")
def define(word: str=typer.Argument(..., help="Word to search"),
           short: bool = typer.Option(False, help="Lightweight definitions.")):
    
    """📚 [bold blue]Lookup[/bold blue] a word in the dictionary"""
    
    print(f"[blue]{word}[/blue]")
    print("[bold]DEFINITION: [/bold]")
    if short:
        Dictionary.lookup(word, short=True)
    if not short:
        Dictionary.lookup(word, short=False)



if __name__ == "__main__":
    app()