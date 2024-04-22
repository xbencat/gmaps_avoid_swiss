=====
Usage
=====

Including Extra Fields
----------------------

To request specific extra fields in the response, list them in the ``extra_fields`` in ``compute_route()`` parameter using dot notation. Here are examples of how to include detailed nested fields:

- To include the token for the route: ``['routes.routeToken']``
- To include the encoded polyline: ``['routes.polyline.encodedPolyline']``
- Both: ``['routes.polyline.encodedPolyline', 'routes.routeToken']``

By default, these will be in the response always, unless you override them in route handler
``['routes.distanceMeters', 'routes.duration', 'routes.polyline.encodedPolyline']``

This notation allows users to specify precise components of the structured data they wish to include in the API response.

For all the possible fields, check out official google documentation:

https://developers.google.com/maps/documentation/routes/reference/rest/v2/TopLevel/computeRoutes#response-body

Response Example
----------------

Response::

      routes {
        distance_meters: 869010
        duration {
          seconds: 36653
        }
        polyline {
          encoded_polyline: "gangH}ain@_Au@Sa@Kw@"
        }
      }



Simple Example
--------------
To use GMaps Avoid Swiss Routes in a project try this::



    import time
    import os

    from gmaps_avoid_swiss.client import GMapsRoutingClient
    from gmaps_avoid_swiss.routes import RoutesHandler


    def compute_route(api_key, origin_data, destination_data):
        try:
            client = GMapsRoutingClient(api_key)
            routes_handler = RoutesHandler(client)
            response = routes_handler.compute_route(origin_data, destination_data)
            print(response.routes[0].response.routes[0].polyline.encoded_polyline)
        except Exception as e:
            print(f"An error occurred: {e}")


    def main():
        api_key = os.getenv("GOOGLE_MAPS_API_KEY", "AIzarreeeeeeeeeeeeee")

        origin_data = {"lat": 48.5734, "lng": 7.7521}  # Strasbourg
        destination_data = {"lat": 45.4637, "lng": 9.1885}  # Milan

        start_time = time.perf_counter()
        compute_route(api_key, origin_data, destination_data)
        end_time = time.perf_counter()
        print(f"Execution time: {end_time - start_time:.3f} seconds")


    if __name__ == '__main__':
        main()


Some examples are also in github `repository`_.

.. _repository: https://github.com/xbencat/gmaps_avoid_swiss
