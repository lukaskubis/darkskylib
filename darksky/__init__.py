from builtins import dict
from builtins import str

from .forecast import Forecast


def forecast(*params, **kwparams):

    # required params as a dictionary
    if len(params) == 1:
        if not isinstance(params[0], dict):
            msg = "'params' not a dictionary ({})".format(type(params))
            raise AttributeError(msg)
        params = params[0]

    # location as a string query
    elif len(params) == 2:
        try:
            from geopy.geocoders import Nominatim
        except ImportError:
            msg = "Required library not installed: 'geopy'"
            raise ImportError(msg)

        key, address = params
        location = Nominatim().geocode(address)
        params = dict(
            key = key,
            latitude = location.latitude,
            longitude = location.longitude
        )

    # required params as positional arguments
    elif len(params) == 3:
        params = dict(
            key = params[0],
            latitude = params[1],
            longitude = params[2]
        )

    # conflicting location parameters
    else:
        args = len(params)
        msg = "forecast() doesn't take {} positional arguments".format(args)
        raise AttributeError(msg)

    # merge default and explicit params
    parameters = dict(params, **kwparams)

    # split required and optional params
    try:
        key = parameters.pop('key')
        latitude = parameters.pop('latitude')
        longitude = parameters.pop('longitude')
    except KeyError as err:
        msg = 'Missing parameter: {}'.format(err)
        raise AttributeError(msg)

    return Forecast(key, latitude, longitude, **parameters)
