=====
Usage
=====

To use GMaps Avoid Swiss Routes in a project::


    import json

    from gmaps_avoid_swiss import GMapsRoutingClient


    def main():
        api_key = "your_api_key"
        client = GMapsRoutingClient(api_key)

        origin_data = {'address': 'New York, NY, USA'}
        destination_data = {'address': 'New Jersey, NJ, USA'}

        response = client.compute_route(origin_data, destination_data)

        print(response.routes[0].distance_meters)
        print(response.routes[0].duration)
        print(response.routes[0].polyline)


    if __name__ == '__main__':
        start_time = time.perf_counter()
        main()
        end_time = time.perf_counter()  # End timing
        print(f"Execution time: {end_time - start_time:.3f} seconds")

