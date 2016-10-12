from builtins import dict
from builtins import str

from .forecast import Forecast


def forecast(*params, **kwparams):
    if len(params) == 1:
        # required params as a dictionary
        if not isinstance(params[0], dict):
            msg = "'params' not a dictionary ({})".format(type(params))
            raise AttributeError(msg)
        params = params[0]
    elif len(params) == 3:
        # required params as positional arguments
        params = dict(
            key = params[0],
            latitude = params[1],
            longitude = longitude[2]
        )
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
