from rich import print
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
import time
from rich.progress import track
from rich.syntax import Syntax



def print_about_app()->None:
    """
    Prints the about app page
    1. Create a layout object
    2. Create a header content object with the help of the Panel class
    3. Create a footer content object with the help of the Panel class
    4. Create a main content object with the help of the Panel class
    5. Divide the "screen" into three parts
    6. Update the header, main and footer with their respective content objects
    7. Print the layout which contains details about the app 
    """
    layout = Layout()  
    
    header_content =  Panel(
        renderable="📚 [gold1 bold]VocabularyCLI[/gold1 bold] is a lightweight [i u]Command Line Interface[/i u] that allows users to look up word definitions, examples, synonyms and antonyms directly via the command line. Powered with several utility based commands our CLI offers rapid and robust Knowledge Base capabilities like [b]Flashcards, Tagging, Word Management, Graph Reporting, Bulk import and export of word lists[/b] and is a definitive software for linguaphiles.\n\n💻 This application boasts a simple and intuitive interface that is easy to use and is a must have for anyone who wants to expand their vocabulary and improve their language skills. The app also offers advanced [b]Text Classification and Processing[/b] via the use of Natural Language Processing and Machine Learning algorithms.\n\n💎 This CLI showcases eye-catching Panels, Tables, Animated Symbols, Emojis, Interactive Menus, Spinners, Colored fonts and other rich features that will make the user learning experience more enjoyable and interactive.",
        title="[reverse]ABOUT VOCABULARY CLI[/reverse]",
        title_align="center",
        border_style="bold green",
        padding=(1,1),
        box= box.DOUBLE_EDGE,
        highlight=True
        )


    footer_content = Panel(
        renderable="\n    👩‍💻 [b reverse]Source[/b reverse]: [link=https://github.com/HighnessAtharva/VocabularyBuilderCLI]GitHub[/link]\t\t\t    📚 [b reverse]Docs[/b reverse]: [link=https://github.com/HighnessAtharva/VocabularyBuilderCLI]Read[/link]\t\t\t   🌐 [b reverse]Website[/b reverse]: [link=https://vocabcli.github.io/]Explore[/link]\t\t\t   🚀 [b reverse]Demo[/b reverse]: [link=https://vocabcli.github.io/]View[/link]\n",
        title="[reverse]THANK YOU FOR USING THIS APP[/reverse]",
        title_align="center",
        border_style="bold violet",
        padding=(1,0),
        box= box.DOUBLE_EDGE,
        highlight=True
        )

    main_content = Panel(
        renderable="[bold u]WE HAVE[/bold u]:\n\n[bold green]1.[/bold green] Dictionary and Thesaurus Lookups\n[bold green]2.[/bold green] Word Management\n[bold green]3.[/bold green] Quote Saving\n[bold green]4.[/bold green] Import and Export\n[bold green]5.[/bold green] Rich Markup\n[bold green]6.[/bold green] Graph Reporting\n[bold green]7.[/bold green] Flashcard Generation\n[bold green]8.[/bold green] Natural Language Processing\n[bold green]9.[/bold green] Word Quizzes\n[bold green]10.[/bold green] Sentiment Analysis\n[bold green]11.[/bold green] Paraphrasing and Plagarism Detection\n🌟 a lot more...",
        title="[reverse]FEATURES[/reverse]",
        title_align="center",
        border_style="bold blue",
        padding=(1,1),
        box= box.DOUBLE_EDGE,
        )


    # Divide the "screen" in to three parts
    layout.split(
        Layout(name="header", size=14),
        Layout(name="main", size=18),
        Layout(name="footer", size=6),
    )

    #HEADER
    layout["header"].update(
    header_content
    )


    # MAIN CONTENT
    layout["main"].split_row(
        Layout(name="side",),
        Layout(
            main_content,
            name="body", ratio=2),
    )


    # SIDE CONTENT
    layout["side"].split(
            # SIDE CONTENT TOP
            Layout(
               Panel(renderable="\t\t  💲💲💲 \n\n       [b u]DONATIONS AND SUPPORT IS WELCOME[/b u] \n\n    [b u]PLEASE VISIT OUR GITHUB SPONSORS PAGE[/b u] \n\n \t\t  💰💰💰", border_style="green")
            ),

            # SIDE CONTENT BOTTOM
            Layout(
                Panel("🐍 [b u]Developed with[/b u]: Python, Typer, Rich, PyTest, Seaborn\n\n😎 [b u]Copyright[/b u]: 2022 (Atharva Shah, Anay Deshpande)\n\n✅ [b u]Language Support[/b u]: English", border_style="red")
            )
    )

    # FOOTER
    layout["footer"].update(
        footer_content
    )


    print(layout)