import unittest
from unittest.mock import patch, MagicMock
from shapely.geometry import LineString, Polygon
import json

from gmaps_avoid_swiss.geo_check import GeographicChecker


class TestGeographicChecker(unittest.TestCase):
    def setUp(self):
        swiss_coords = [(6, 46), (8, 46), (8, 48), (6, 48), (6, 46)]
        swiss_polygon = Polygon(swiss_coords)
        self.geo_checker = GeographicChecker()
        self.geo_checker.swiss_polygon = swiss_polygon

    def test_initialization_loads_swiss_polygon(self):
        self.assertIsInstance(self.geo_checker.swiss_polygon, Polygon)

    def test_is_point_in_swiss(self):
        point_inside = self.geo_checker.is_point_in_swiss(47.0, 7.0)
        point_outside = self.geo_checker.is_point_in_swiss(50.0, 10.0)
        self.assertTrue(point_inside)
        self.assertFalse(point_outside)

    def test_does_route_cross_swiss(self):
        with patch('polyline.polyline.decode', return_value=[(8.0, 47.0), (8.5, 47.5)]):
            path = MagicMock(encoded_polyline="_p~iF~ps|U_ulLnnqC_mqNvxq`@")
            self.assertTrue(self.geo_checker.does_route_cross_swiss(path))

    def test_sort_cities_by_distance(self):
        intersection = LineString([(6.0, 46.0), (9.0, 47.0)])
        self.geo_checker.sort_cities_by_distance(intersection)
        self.assertEqual(self.geo_checker.cities[0]['city']['lat'], 47.2692)
