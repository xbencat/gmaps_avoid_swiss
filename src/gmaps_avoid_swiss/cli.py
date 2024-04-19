
"""Console script for gmaps_avoid_swiss."""
import typer
from rich.console import Console
from .gmaps_avoid_swiss import GMapsRoutingClient

app = typer.Typer()
console = Console()


@app.command()
def compute_route(api_key: str, origin: str, destination: str):
    """
    Compute the route from origin to destination using the GMapsRoutingClient.

    Args:
        api_key (str): The Google Maps API key for authentication.
        origin (str): The origin location (address, place ID, or coordinates).
        destination (str): The destination location (address, place ID, or coordinates).
    """
    client = GMapsRoutingClient(api_key)
    origin_data = {'address': origin}
    destination_data = {'address': destination}

    response = client.compute_route(origin_data, destination_data)
    console.print("[bold green]Route Computed Successfully![/]")
    console.print(response, justify="center")


if __name__ == "__main__":
    app()
