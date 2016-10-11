from builtins import dict
from builtins import str

from .forecast import Forecast


def forecast(params={}, **kwparams):
    if not isinstance(params, dict):
        raise TypeError("'forecast': params not in dictionary.")

    # merge default and explicit params
    parameters = dict(params, **kwparams)

    # set mandatory parameters here
    key = parameters.pop('key', None)
    latitude = parameters.pop('latitude', None)
    longitude = parameters.pop('longitude', None)

    # Required parameters are missing
    for param in ('key', 'latitude', 'longitude'):
        if not eval(param):
            raise ValueError('Missing parameter: ' + param)

    return Forecast(key, latitude, longitude, **parameters)
