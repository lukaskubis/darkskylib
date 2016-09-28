from builtins import dict
from builtins import str

from .forecast import Forecast


def forecast(settings={}, **kwsettings):
    # merge default and explicit settings
    fcsettings = dict(settings, **kwsettings)

    # set mandatory parameters here
    api_key = fcsettings.pop('api_key', None)
    latitude = fcsettings.pop('latitude', None)
    longitude = fcsettings.pop('longitude', None)

    # Don't even try to construct the forecast if mandatory params are missing
    for key in ('api_key', 'latitude', 'longitude'):
        if not eval(key):
            raise ValueError('Missing parameter: ' + key)

    return Forecast(api_key, latitude, longitude, **fcsettings)
