# __init__.py

from .forecast import Forecast


def forecast(key, lat, lng, time=None, **queries):
    return Forecast(key, lat, lng, time, **queries)
