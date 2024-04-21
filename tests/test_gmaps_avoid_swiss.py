import unittest

from unittest.mock import patch, MagicMock

from gmaps_avoid_swiss import RoutesHandler
from gmaps_avoid_swiss.client import GMapsRoutingClient


class TestGMapsRoutingClient(unittest.TestCase):

    @patch('gmaps_avoid_swiss.geo_check.GeographicChecker.does_route_cross_swiss')
    @patch('gmaps_avoid_swiss.client.routing_v2.RoutesClient')
    def test_compute_route(self, MockRoutesClient, mock_does_route_cross_swiss):
        valid_polyline = '_p~iF~ps|U_ulLnnqC_mqNvxq`@'
        mock_does_route_cross_swiss.return_value = False
        mock_response = MagicMock()
        mock_response.routes = [MagicMock(
            distance_meters=1000,
            duration=MagicMock(seconds=3600),
            polyline=MagicMock(encoded_polyline=valid_polyline))]

        mock_client = MockRoutesClient.return_value
        mock_client.compute_routes.return_value = mock_response

        client = GMapsRoutingClient("AIza-api_key")
        origin = {"lat": 48.5734, "lng": 7.7521}  # Strasbourg
        destination = {"lat": 45.4637, "lng": 9.1885}  # Milan
        routes_handler = RoutesHandler(client)
        response = routes_handler.compute_route(origin, destination)

        self.assertTrue(response.routes)
        self.assertEqual(response.routes[0].distance_meters, 1000)
        self.assertEqual(response.routes[0].duration.seconds, 3600)
        mock_does_route_cross_swiss.assert_called_once_with(mock_response.routes[0].polyline)
