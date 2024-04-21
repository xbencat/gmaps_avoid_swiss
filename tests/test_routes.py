import unittest
from unittest.mock import patch, MagicMock

from gmaps_avoid_swiss.client import GMapsRoutingClient
from gmaps_avoid_swiss.routes import RoutesHandler
from gmaps_avoid_swiss.waypoints import create_waypoint


class TestRoutesHandler(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock(spec=GMapsRoutingClient)
        self.handler = RoutesHandler(self.client)

    def test_compute_route(self):
        origin = {"lat": 47.3769, "lng": 8.5417}  # Example location in Zurich
        destination = {"lat": 46.9480, "lng": 7.4474}  # Example location in Bern

        self.handler._perform_route_computation = MagicMock(return_value='Simulated ComputeRoutesResponse')

        response = self.handler.compute_route(origin, destination)

        self.assertEqual(response, 'Simulated ComputeRoutesResponse')
        self.handler._perform_route_computation.assert_called_once()

    def test_is_any_location_inside_swiss(self):
        with patch.object(self.handler.geo_checker, 'is_point_in_swiss', return_value=True):
            locations = [{"lat": 47.3769, "lng": 8.5417}, {"lat": 50.1109, "lng": 8.6821}]
            result = self.handler._is_any_location_inside_swiss(locations)
            self.assertTrue(result)

    def test_merge_fields(self):
        extra_fields = ['routes.distanceMeters', 'routes.polyline.encodedPolyline']
        result = self.handler._merge_fields(extra_fields)
        self.assertEqual(set(result), {'routes.duration', 'routes.distanceMeters', 'routes.polyline.encodedPolyline'})
