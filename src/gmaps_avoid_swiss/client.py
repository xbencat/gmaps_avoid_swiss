from google.maps import routing_v2
from google.api_core.client_options import ClientOptions


class GMapsRoutingClient:
    """Client for Google Maps Routing API V2 that uses an API key for authentication."""

    def __init__(self, api_key: str):
        """
        Initialize the GMapsRoutingClient with an API key.

        :param api_key: The Google Maps API key for authentication.
        :type api_key: str
        """
        client_options = ClientOptions(api_key=api_key)
        self.client = routing_v2.RoutesClient(client_options=client_options)

        if api_key and not api_key.startswith("AIza"):
            raise ValueError("Invalid API key provided.")
