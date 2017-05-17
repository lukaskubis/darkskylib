# __init__.py

from .forecast import Forecast

def forecast(key, lat, lng, **queries):
    return Forecast(key, lat, lng, **queries)
