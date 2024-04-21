.. _geos:
.. include:: ../GEOS.rst

GEOS Dependency
=====================================
GEOS (Geometry Engine - Open Source) is a C++ library that supports spatial operations in various GIS software and libraries, such as Shapely—a Python package used for geometric object manipulation. GEOS implements the OpenGIS Simple Features for SQL, essential for operations like area calculation, intersections, and other spatial analyses in Shapely. For Shapely to function correctly, GEOS must be installed and configured in your environment.

How to Install GEOS
-------------------

The installation of GEOS varies depending on your operating system:

For macOS
~~~~~~~~~

You can install GEOS using Homebrew:

.. code-block:: bash

    brew install geos

For Ubuntu/Debian
~~~~~~~~~~~~~~~~~

You can install GEOS from the package manager:

.. code-block:: bash

    sudo apt-get install libgeos-dev

For Windows
~~~~~~~~~~~

Installing GEOS on Windows can be more complex because it involves setting up the library manually unless you use a package manager like Conda, which simplifies it:

.. code-block:: bash

    conda install -c conda-forge geos

