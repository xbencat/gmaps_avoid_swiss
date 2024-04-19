from google.maps import routing_v2
from google.maps.routing_v2.types import ComputeRoutesRequest
from google.api_core.client_options import ClientOptions

from src.gmaps_avoid_swiss.waypoints import create_waypoint


class GMapsRoutingClient:
    """Client for Google Maps Routing API V2 that uses an API key for authentication."""

    def __init__(self, api_key: str):
        """
        Initialize the GMapsRoutingClient with an API key.

        Args:
            api_key (str): The Google Maps API key for authentication.
        """
        client_options = ClientOptions(api_key=api_key)
        self.client = routing_v2.RoutesClient(client_options=client_options)

    def compute_route(self, origin: dict, destination: dict) -> routing_v2.ComputeRoutesResponse:
        """
        Compute the route from origin to destination using simple dict inputs.

        Args:
            origin (dict): A dictionary containing the origin location data.
            destination (dict): A dictionary containing the destination location data.

        Returns:
            routing_v2.ComputeRoutesResponse: The response containing the computed routes.

        Raises:
            Exception: If there is an error while computing the routes.
        """
        origin_waypoint = create_waypoint(origin)
        destination_waypoint = create_waypoint(destination)

        request = ComputeRoutesRequest(
            origin=origin_waypoint,
            destination=destination_waypoint
        )

        paths = "routes.distanceMeters,routes.duration,routes.polyline.encodedPolyline"

        try:
            response = self.client.compute_routes(request=request, metadata=[("x-goog-fieldmask", paths)])
            return response
        except Exception as e:
            raise Exception(f"Failed to compute routes: {e}")
