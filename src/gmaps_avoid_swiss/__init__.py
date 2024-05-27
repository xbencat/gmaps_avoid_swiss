"""Top-level package for GMaps Avoid Swiss Routes."""

__author__ = """Gregor Bencat"""
__email__ = 'bencat.gregor@gmail.com'
__version__ = '0.1.10'

from gmaps_avoid_swiss.client import GMapsRoutingClient
from gmaps_avoid_swiss.routes import RoutesHandler

__all__ = ["GMapsRoutingClient", "RoutesHandler"]
