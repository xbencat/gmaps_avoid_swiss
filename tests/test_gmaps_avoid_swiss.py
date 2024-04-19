import unittest

from unittest.mock import patch
from gmaps_avoid_swiss.client import GMapsRoutingClient


class TestGMapsRoutingClient(unittest.TestCase):

    @patch('src.gmaps_avoid_swiss.client.routing_v2.RoutesClient')
    def test_compute_route(self, mock_routes_client):
        mock_response = unittest.mock.Mock()
        mock_response.routes = [unittest.mock.Mock(distance_meters=1000, duration=unittest.mock.Mock(seconds=3600))]
        mock_routes_client.return_value.compute_routes.return_value = mock_response

        client = GMapsRoutingClient("api_key")
        origin = {"address": "New York, NY, USA"}
        destination = {"address": "New Jersey, NJ, USA"}
        response = client.compute_route(origin, destination)

        self.assertTrue(response.routes)
        self.assertGreater(response.routes[0].distance_meters, 0)
        self.assertGreater(response.routes[0].duration.seconds, 0)
