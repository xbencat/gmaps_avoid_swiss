import json
from importlib import resources
from typing import Union

from google.maps.routing_v2 import Polyline
from polyline import polyline
from shapely import MultiLineString
from shapely.geometry import shape, Point, Polygon, LineString


class GeographicChecker:
    INNSBRUCK = {"lat": 47.2692, "lng": 11.4041}
    LION = {"lat": 45.7640, "lng": 4.8357}
    BEAUNE = {"lat": 47.0260, "lng": 4.8400}
    FREIBURG = {"lat": 47.9990, "lng": 7.8421}

    def __init__(self):
        """
        Initialize the GeographicChecker with a predefined polygon of Switzerland.
        """
        self.swiss_geojson = "switzerland.geojson"
        # Define the boundary of Switzerland using a geojson.
        self.swiss_polygon = self._load_switzerland_boundary()
        self.cities = []

    def is_point_in_swiss(self, lat: float, lng: float) -> bool:
        """
        Check if a geographic point is within Switzerland.

        :param lat: Latitude of the point.
        :type lat: float
        :param lng: Longitude of the point.
        :type lng: float
        :return: True if the point is within the polygon of Switzerland, False otherwise.
        :rtype: bool
        """
        point = Point(lng, lat)
        return self.swiss_polygon.contains(point)

    def does_route_cross_swiss(self, path: Polyline) -> LineString:
        """
        Determine whether a route, defined by a polyline (encoded string or GeoJSON), crosses Switzerland.

        :param path: Polyline data which could be an encoded string or a GeoJSON object.
        :type path: Polyline
        :return: True if the route crosses through Switzerland, False otherwise.
        :rtype: bool
        """

        try:
            points = polyline.decode(path.encoded_polyline, geojson=True)
        except AttributeError:
            raise ValueError("Missing or invalid 'encoded_polyline' attribute.")
        except Exception as e:
            raise ValueError(f"Error decoding polyline: {str(e)}")

        route_linestring = LineString(points)

        return self.swiss_polygon.intersection(route_linestring)

    def sort_cities_by_distance(self, intersection: Union[LineString, MultiLineString]):
        """
        Sort the cities based on their total distance to the start and end points of the intersection with Switzerland.

        :param intersection: The LineString representing the intersection of the route with Switzerland.
        :type intersection: LineString
        """

        self.cities.clear()

        if isinstance(intersection, LineString):
            start = Point(intersection.coords[0])  # Start of LineString
            end = Point(intersection.coords[-1])  # End of LineString
        elif isinstance(intersection, MultiLineString):
            start = Point(intersection.geoms[0].coords[0])  # First point of the first LineString
            end = Point(intersection.geoms[-1].coords[-1])  # Last point of the last LineString
        else:
            raise TypeError("Unsupported geometry type for intersection")

        for city in [self.INNSBRUCK, self.LION, self.BEAUNE, self.FREIBURG]:
            city_point = Point(city['lng'], city['lat'])

            distance_to_start = start.distance(city_point)
            distance_from_end = end.distance(city_point)
            total_distance = distance_to_start + distance_from_end
            self.cities.append({'city': city, 'dist': total_distance})

        # Sort cities by the total distance
        self.cities.sort(reverse=True, key=lambda x: x['dist'])

    def _load_switzerland_boundary(self):
        """
        Load the boundary of Switzerland from a GeoJSON file.

        :return: A Shapely Polygon object representing the boundary of Switzerland.
        :rtype: Polygon
        :raises FileNotFoundError: If the GeoJSON file could not be found.
        :raises json.JSONDecodeError: If there is an error decoding the GeoJSON.
        :raises RuntimeError: If there is an unexpected error during the file loading or parsing.
        """
        try:
            with resources.open_text('gmaps_avoid_swiss.data', self.swiss_geojson) as file:
                data = json.load(file)
            feature = data['features'][0]
            polygon = shape(feature['geometry'])
            return polygon
        except FileNotFoundError:
            raise FileNotFoundError("The GeoJSON file could not be found.")
        except json.JSONDecodeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to load or parse the GeoJSON file: {e}")
