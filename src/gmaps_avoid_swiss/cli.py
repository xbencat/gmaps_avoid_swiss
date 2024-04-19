"""Console script for gmaps_avoid_swiss."""
import gmaps_avoid_swiss

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for gmaps_avoid_swiss."""
    message = gmaps_avoid_swiss.hello_world()
    console.print(message)


if __name__ == "__main__":
    app()
