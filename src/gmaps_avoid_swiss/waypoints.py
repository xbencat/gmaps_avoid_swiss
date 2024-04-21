from google.maps.routing_v2.types import Waypoint, Location
from google.type import latlng_pb2


def create_waypoint(location_data: dict) -> Waypoint:
    """
    Create a Waypoint object from the provided location data.

    :param location_data: A dictionary containing location information. It should have one of the following keys:
        - 'lat' and 'lng' for latitude and longitude coordinates
        - 'place_id' for a Google Maps place ID
        - 'address' for a textual address
    :type location_data: dict

    :return: A Waypoint object created from the location data.
    :rtype: Waypoint

    :raises ValueError: If the provided location data is invalid.
    """
    if 'lat' in location_data and 'lng' in location_data:
        return _create_waypoint_from_coordinates(
            location_data['lat'], location_data['lng']
        )
    else:
        raise ValueError("Currently, only latitude and longitude coordinates are accepted. "
                         "Please provide a dictionary with 'lat' and 'lng' keys.")
    # elif 'place_id' in location_data:
    #     return _create_waypoint_from_place_id(location_data['place_id'])
    # elif 'address' in location_data:
    #     return _create_waypoint_from_address(location_data['address'])
    # else:
    #     raise ValueError("Invalid location data provided")


def _create_waypoint_from_coordinates(latitude: float, longitude: float) -> Waypoint:
    """
    Create a Waypoint object from latitude and longitude coordinates.

    :param latitude: The latitude coordinate.
    :type latitude: float
    :param longitude: The longitude coordinate.
    :type longitude: float

    :return: A Waypoint object created from the coordinates.
    :rtype: Waypoint
    """
    lat_lng = latlng_pb2.LatLng(latitude=latitude, longitude=longitude)
    location = Location(lat_lng=lat_lng)
    return Waypoint(location=location)


def _create_waypoint_from_place_id(place_id: str) -> Waypoint:
    """
    Create a Waypoint object from a Google Maps place ID.

    :param place_id: The Google Maps place ID.
    :type place_id: str

    :return: A Waypoint object created from the place ID.
    :rtype: Waypoint
    """
    return Waypoint(place_id=place_id)


def _create_waypoint_from_address(address: str) -> Waypoint:
    """
    Create a Waypoint object from a textual address.

    :param address: The textual address.
    :type address: str

    :return: A Waypoint object created from the address.
    :rtype: Waypoint
    """
    return Waypoint(address=address)
