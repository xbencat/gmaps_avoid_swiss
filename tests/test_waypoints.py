import unittest
from google.maps.routing_v2.types import Waypoint
from gmaps_avoid_swiss.waypoints import create_waypoint, _create_waypoint_from_coordinates, \
    _create_waypoint_from_place_id, _create_waypoint_from_address


class TestWaypoints(unittest.TestCase):
    def test_create_waypoint_from_coordinates(self):
        waypoint = _create_waypoint_from_coordinates(40.7128, -74.0060)
        self.assertIsInstance(waypoint, Waypoint)
        self.assertEqual(waypoint.location.lat_lng.latitude, 40.7128)
        self.assertEqual(waypoint.location.lat_lng.longitude, -74.0060)

    def test_create_waypoint_from_place_id(self):
        waypoint = _create_waypoint_from_place_id("ChIJOwg_06VPwokRYv534QaPC8g")
        self.assertIsInstance(waypoint, Waypoint)
        self.assertEqual(waypoint.place_id, "ChIJOwg_06VPwokRYv534QaPC8g")

    def test_create_waypoint_from_address(self):
        waypoint = _create_waypoint_from_address("New York, NY, USA")
        self.assertIsInstance(waypoint, Waypoint)
        self.assertEqual(waypoint.address, "New York, NY, USA")

    def test_create_waypoint_invalid_data(self):
        with self.assertRaises(ValueError):
            create_waypoint({})
