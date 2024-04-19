"""Console script for gmaps_avoid_swiss."""
import gmaps_avoid_swiss

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for gmaps_avoid_swiss."""
    console.print("Replace this message by putting your code into "
               "gmaps_avoid_swiss.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
