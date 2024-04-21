import time
import os

from gmaps_avoid_swiss.client import GMapsRoutingClient
from gmaps_avoid_swiss.routes import RoutesHandler


def compute_route(api_key, origin_data, destination_data):
    try:
        client = GMapsRoutingClient(api_key)
        routes_handler = RoutesHandler(client)
        response = routes_handler.compute_route(origin_data, destination_data)
        print(response.routes[0].duration)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaxxxxxxxxxxxxxxxx")

    origin_data = {"lat": 48.5734, "lng": 7.7521}  # Strasbourg
    destination_data = {"lat": 45.4637, "lng": 9.1885}  # Milan

    start_time = time.perf_counter()
    compute_route(api_key, origin_data, destination_data)
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.3f} seconds")


if __name__ == '__main__':
    main()
