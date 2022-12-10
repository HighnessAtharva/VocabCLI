from rich import print
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align


def print_about_app():
    """Prints the details of the app"""

    layout = Layout()

    header_content =  Panel(
        renderable="[bold gold1]VocabularyBuilder[/bold gold1] is a [i]Lightweight CLI[/i] for Dictionary Lookups, Vocabulary Building, Quote Saving and enhancing Knowledge Base. Supported with Rich Markup, Graph Reporting and Flashcard Generation",
        title="[reverse]ABOUT VOCABULARY CLI[/reverse]",
        title_align="center",
        border_style="bold green",
        padding=(2,2),
        box= box.DOUBLE_EDGE,
        highlight=True
        )


    footer_content = Panel(
        renderable="Developed using: Python, Typer, Rich, Matplotlib, Pytest\nCopyright: © 2022 (Atharva Shah, Anay Deshpande)\nSource: [link=https://github.com/HighnessAtharva/VocabularyBuilderCLI]GitHub[/link]",
        title="[reverse]THANK YOU FOR USING THIS APP[/reverse]",
        title_align="center",
        border_style="bold violet",
        padding=(1,1),
        box= box.DOUBLE_EDGE,
        highlight=True
        )

    main_content = Panel(
        renderable="[bold u]WE HAVE[/bold u]:\n\n[bold green]1.[/bold green] Dictionary Lookups\n[bold green]2.[/bold green] Vocabulary Building\n[bold green]3.[/bold green] Quote Saving\n[bold green]4.[/bold green] Knowledge Base\n[bold green]5.[/bold green] Rich Markup\n[bold green]6.[/bold green] Graph Reporting\n[bold green]7.[/bold green] Flashcard Generation",
        title="[reverse]FEATURES[/reverse]",
        title_align="center",
        border_style="bold blue",
        padding=(1,1),
        box= box.DOUBLE_EDGE,
        )


    # Divide the "screen" in to three parts
    layout.split(
        Layout(name="header", size=7),
        Layout(name="main", size=15),
        Layout(name="footer", size=7),
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
                Panel("Hello", border_style="green")
            ),

            # SIDE CONTENT BOTTOM
            Layout(
                Panel("Hello", border_style="red")
            )
    )

    # FOOTER
    layout["footer"].update(
        footer_content
    )


    print(layout)
