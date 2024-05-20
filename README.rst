========================
GMaps Avoid Swiss Routes
========================


.. image:: https://img.shields.io/pypi/v/gmaps_avoid_swiss.svg
        :target: https://pypi.python.org/pypi/gmaps_avoid_swiss

.. image:: https://readthedocs.org/projects/gmaps-avoid-swiss/badge/?version=latest
        :target: https://gmaps-avoid-swiss.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A Python package that customizes Google Maps routing to avoid Swiss routes unless the origin, destination, or waypoints include locations within Switzerland.


* Free software: MIT license
* Documentation: https://gmaps-avoid-swiss.readthedocs.io.


Dependencies
____________

This package requires the GEOS library as it utilizes Shapely for geographic operations.
For installation instructions and more details, please refer to `Geos <geos.html>`_ page.


Features
--------

* Calculates duration, transit time, and encoded path from origin to destination
* Avoids routing through Switzerland by trying alternative routes or dynamically selecting alternative cities
  - If the initial route or alternative routes intersects with Switzerland, the system optimizes the route by selecting intermediate cities to avoid crossing Swiss borders
  - The cities are prioritized based on their proximity to the intersection points with Switzerland
  - The system iteratively tries different cities until a route that doesn't pass through Switzerland is found
  - If no valid route is found after exhausting all city options, the system falls back to the original route
* Right now its only possible to use address in format :code:`{"lat": 48.5734, "lng": 7.7521}`

To-Do List
----------

* Add opting out of avoiding Swiss.
* Improve Swiss route avoidance algorithms.

Credits
-------

This package was created with Cookiecutter_ .

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
