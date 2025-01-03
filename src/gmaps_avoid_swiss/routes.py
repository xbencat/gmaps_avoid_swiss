from google.maps import routing_v2
from google.maps.routing_v2.types import (
    ComputeRoutesRequest,
    RouteModifiers,
)
from gmaps_avoid_swiss.client import GMapsRoutingClient
from gmaps_avoid_swiss.geo_check import GeographicChecker
from gmaps_avoid_swiss.waypoints import create_waypoint


class RoutesHandler:
    """
    Handles routing functionalities for GMapsRoutingClient.
    """
    geo_checker = GeographicChecker()

    def __init__(self, client: GMapsRoutingClient, default_fields: list = None):
        """
        Initialize RoutesHandler with a GMapsRoutingClient instance and default fields.

        :param client: An instance of GMapsRoutingClient.
        :type client: GMapsRoutingClient
        :param default_fields: Default fields to include in the API's response. If not specified,
                               a predefined set of fields is used.
        :type default_fields: list, optional
        """
        self.client = client
        # If no fields are specified, use a basic set of fields as the default
        if default_fields is None:
            default_fields = ['routes.distanceMeters', 'routes.duration', 'routes.polyline.encodedPolyline']
        self.default_fields = default_fields

    def compute_route(
        self,
        origin: dict,
        destination: dict,
        extra_fields: list = None,
        avoid_ferries: bool = False,
        avoid_tolls: bool = False,
        avoid_highways: bool = False,
    ) -> routing_v2.ComputeRoutesResponse:
        """
        Compute the route from origin to destination with customizable response fields.
        Extends the default fields with any extra fields specified for this particular call.
        For detailed information on all available extra fields, refer to the corresponding section
        in the user guide.

        :param origin: A dictionary containing the origin location data.
        :type origin: dict
        :param destination: A dictionary containing the destination location data.
        :type destination: dict
        :param extra_fields: Additional fields to include in the response, in addition to default fields.
        :type extra_fields: list, optional
        :param avoid_ferries: Whether to avoid ferries in the computed route.
        :type avoid_ferries: bool
        :param avoid_tolls: Whether to avoid toll roads.
        :type avoid_tolls: bool
        :param avoid_highways: Whether to avoid highways.
        :type avoid_highways: bool
        :return: The response containing the computed routes.
        :rtype: routing_v2.ComputeRoutesResponse
        :raises Exception: If there is an error while computing the routes.
        """

        origin_waypoint = create_waypoint(origin)
        destination_waypoint = create_waypoint(destination)

        route_fields = self._merge_fields(extra_fields)
        field_mask = ",".join(route_fields)

        request = ComputeRoutesRequest(
            origin=origin_waypoint,
            destination=destination_waypoint,
            route_modifiers=RouteModifiers(
                avoid_ferries=avoid_ferries,
                avoid_tolls=avoid_tolls,
                avoid_highways=avoid_highways
            ),
        )

        if self._is_any_location_inside_swiss([origin, destination]):
            return self._perform_route_computation(request, field_mask)
        else:
            return self._handle_routing_around_swiss(request, field_mask)

    def _is_any_location_inside_swiss(self, locations: list) -> bool:
        """
        Check if any location in the list is within Switzerland.

        :param locations: A list of dictionaries each containing latitude and longitude.
        :type locations: list
        :return: True if any location is inside Switzerland, otherwise False.
        :rtype: bool
        """
        for location in locations:
            lat = location['lat']
            lng = location['lng']
            if self.geo_checker.is_point_in_swiss(lat, lng):
                return True
        return False

    def _merge_fields(self, extra_fields: list) -> list:
        """
        Merge the default fields with the extra fields, ensuring no duplicates.

        :param extra_fields: Additional fields to include in the response.
        :type extra_fields: list
        :return: The merged list of fields.
        :rtype: list
        """
        if extra_fields:
            return list(set(self.default_fields + extra_fields))
        return self.default_fields[:]

    def _perform_route_computation(self, request: ComputeRoutesRequest,
                                   field_mask: str) -> routing_v2.ComputeRoutesResponse:
        """
        Perform the route computation using the provided ComputeRoutesRequest.

        :param request: The ComputeRoutesRequest containing the route parameters.
        :type request: ComputeRoutesRequest
        :param field_mask: The field mask specifying the fields to include in the response.
        :type field_mask: str

        :return: The response containing the computed routes.
        :rtype: routing_v2.ComputeRoutesResponse

        :raises Exception: If there is an error while computing the routes.
        """
        try:
            response = self.client.client.compute_routes(request=request, metadata=[("x-goog-fieldmask", field_mask)])
            return response
        except Exception as error:
            raise Exception(f"An error occurred: {error}")

    def _handle_routing_around_swiss(self, request: ComputeRoutesRequest,
                                     field_mask: str) -> routing_v2.ComputeRoutesResponse:
        """
        Handle routing when both locations are outside Switzerland but need to check if the route goes through
        Switzerland. If it does, we try alternative routes first, then reroute via common cities.

        :param request: The ComputeRoutesRequest object.
        :type request: ComputeRoutesRequest
        :param field_mask: Field mask for the Google Maps Routing API.
        :type field_mask: Str
        :return: The response from the routing API.
        :rtype: routing_v2.ComputeRoutesResponse
        """

        response = self._perform_route_computation(request, field_mask)
        intersection = self.geo_checker.does_route_cross_swiss(response.routes[0].polyline)

        if intersection:
            alternative_response = self._try_alternative_routes(request, field_mask)

            if alternative_response:
                return alternative_response

            self.geo_checker.sort_cities_by_distance(intersection)
            response = self._reroute_route(request, field_mask)

        return response

    def _reroute_route(self, request: ComputeRoutesRequest, field_mask: str) -> routing_v2.ComputeRoutesResponse:
        """
        Reroute the request through alternative cities to avoid crossing Switzerland.

        :param request: The ComputeRoutesRequest object containing the origin and destination.
        :type request: ComputeRoutesRequest
        :param field_mask: Field mask for the Google Maps Routing API.
        :type field_mask: Str
        :return: The response from the routing API with the rerouted request, or the original response if no valid
                alternative is found.
        :rtype: routing_v2.ComputeRoutesResponse
        """

        response = None
        while self.geo_checker.cities:
            city = self.geo_checker.cities.pop()['city']
            updated_request = self._update_route_request(request, city)
            response = self._perform_route_computation(updated_request, field_mask)

            if not self.geo_checker.does_route_cross_swiss(response.routes[0].polyline):
                break

        if response is None:
            response = self._perform_route_computation(request, field_mask)

        return response

    def _update_route_request(self, request: ComputeRoutesRequest, city: dict) -> ComputeRoutesRequest:
        """
        Update the ComputeRoutesRequest to avoid routes going through Switzerland.

        :param request: The original ComputeRoutesRequest.
        :type request: ComputeRoutesRequest

        :return: The updated ComputeRoutesRequest.
        :rtype: ComputeRoutesRequest
        """
        via = create_waypoint(city)

        updated_request = ComputeRoutesRequest(
            origin=request.origin,
            destination=request.destination,
            intermediates=[via],
        )

        return updated_request

    def _try_alternative_routes(self, request: ComputeRoutesRequest,
                                field_mask: str) -> routing_v2.ComputeRoutesResponse | None:
        """
        Try computing alternative routes to see if any avoid crossing Switzerland.

        :param request: The ComputeRoutesRequest object.
        :type request: ComputeRoutesRequest
        :param field_mask: Field mask for the Google Maps Routing API.
        :type field_mask: str
        :return: The response from the routing API, if a valid alternative is found.
        :rtype: routing_v2.ComputeRoutesResponse
        """
        request.compute_alternative_routes = True

        response = self._perform_route_computation(request, field_mask)
        for route in response.routes:
            if not self.geo_checker.does_route_cross_swiss(route.polyline):
                valid_response = routing_v2.ComputeRoutesResponse()
                valid_response.routes.append(route)
                return valid_response

        return None
