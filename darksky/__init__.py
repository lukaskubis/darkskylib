# __init__.py

from .forecast import Forecast


def forecast(key, latitude, longitude, time=None, **queries):
    return Forecast(key, latitude, longitude, time, **queries)
