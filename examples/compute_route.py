import time
import os

from gmaps_avoid_swiss.client import GMapsRoutingClient
from gmaps_avoid_swiss.routes import RoutesHandler


def compute_route(api_key, origin_data, destination_data):
    client = GMapsRoutingClient(api_key)
    routes_handler = RoutesHandler(client)
    response = routes_handler.compute_route(origin_data, destination_data, avoid_ferries=True)
    print(f"Route: {response}")


def main():
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaxxxxxxxxxxxxxxxx")

    # origin_data = {"lat": 48.5734, "lng": 7.7521}  # Strasbourg
    origin_data = {"lat": 41.1171, "lng": 16.8719}  # Strasbourg
    # destination_data = {"lat": 45.4637, "lng": 9.1885}
    # origin_data = {'lat': 48.1485965, 'lng': 17.1077477}
    # destination_data = {'lat': 41.3874, 'lng': 2.1686}

    # origin_data = {'lat': 39.4699, 'lng': 0.3763}
    # destination_data = {'lat': 48.6217, 'lng': 17.7232}
    destination_data = {'lat': 41.3275, 'lng': 19.8187}

    start_time = time.perf_counter()
    compute_route(api_key, origin_data, destination_data)
    end_time = time.perf_counter()
    print(f"Execution time: {end_time - start_time:.3f} seconds")


if __name__ == '__main__':
    main()
