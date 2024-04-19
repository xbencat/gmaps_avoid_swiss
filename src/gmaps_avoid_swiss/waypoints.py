from google.maps.routing_v2.types import Waypoint, Location
from google.type import latlng_pb2


def create_waypoint(location_data: dict) -> Waypoint:
    """
    Create a Waypoint object from the provided location data.

    Args:
        location_data (dict): A dictionary containing location information.
            It should have one of the following keys:
            - 'lat' and 'lng' for latitude and longitude coordinates
            - 'place_id' for a Google Maps place ID
            - 'address' for a textual address

    Returns:
        Waypoint: A Waypoint object created from the location data.

    Raises:
        ValueError: If the provided location data is invalid.
    """
    if 'lat' in location_data and 'lng' in location_data:
        return _create_waypoint_from_coordinates(
            location_data['lat'], location_data['lng']
        )
    elif 'place_id' in location_data:
        return _create_waypoint_from_place_id(location_data['place_id'])
    elif 'address' in location_data:
        return _create_waypoint_from_address(location_data['address'])
    else:
        raise ValueError("Invalid location data provided")


def _create_waypoint_from_coordinates(latitude: float, longitude: float) -> Waypoint:
    """
    Create a Waypoint object from latitude and longitude coordinates.

    Args:
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.

    Returns:
        Waypoint: A Waypoint object created from the coordinates.
    """
    lat_lng = latlng_pb2.LatLng(latitude=latitude, longitude=longitude)
    location = Location(lat_lng=lat_lng)
    return Waypoint(location=location)


def _create_waypoint_from_place_id(place_id: str) -> Waypoint:
    """
    Create a Waypoint object from a Google Maps place ID.

    Args:
        place_id (str): The Google Maps place ID.

    Returns:
        Waypoint: A Waypoint object created from the place ID.
    """
    return Waypoint(place_id=place_id)


def _create_waypoint_from_address(address: str) -> Waypoint:
    """
    Create a Waypoint object from a textual address.

    Args:
        address (str): The textual address.

    Returns:
        Waypoint: A Waypoint object created from the address.
    """
    return Waypoint(address=address)
