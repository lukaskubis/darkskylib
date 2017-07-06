# __init__.py

from contextlib import contextmanager
from .forecast import Forecast


@contextmanager
def forecast(key, latitude, longitude, time=None, **queries):
    yield Forecast(key, latitude, longitude, time, **queries)
