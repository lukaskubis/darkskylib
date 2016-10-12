from builtins import dict
from builtins import super
from builtins import str

import json
import sys
import requests

from .data import Data_point

class Forecast(Data_point):
    def __init__(self, key, latitude, longitude, **queries):
        self._parameters = dict()
        self.refresh(key=key, latitude=latitude, longitude=longitude, **queries)

    def __setattr__(self, key, value):
        if key in ('_parameters', '_data'):
            return object.__setattr__(self, key, value)
        return super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.currently().keys():
            return self.currently()[key]
        return object.__getattribute__(self, key)

    @property
    def url(self):
        # insert mandatory variables
        params = dict(self._parameters)
        url = 'https://api.darksky.net/forecast/'
        url += params.pop('key') + '/'
        url += str(params.pop('latitude')) + ','
        url += str(params.pop('longitude'))
        if not params:
            return url

        # time machine request
        if 'time' in params.keys():
            url += ',' + str(params.pop('time'))

        # add optional query parameters
        url += '?'
        for key, value in params.items():
            url += key + '=' + str(value) + '&'
        return url

    def refresh(self, params={}, **kwparams):
        if not isinstance(params, dict):
            raise TypeError("'refresh': params not in dictionary.")

        # update request parameters
        self._parameters = dict(self._parameters, **dict(params, **kwparams))

        # request data from API
        try:
            response = requests.get(self.url)
        except requests.exceptions.Timeout:
            print('Error: Timeout')
        except requests.exceptions.TooManyRedirects:
            print('Error: TooManyRedirects')
        except requests.exceptions.RequestException as ex:
            print(ex)
            sys.exit(1)

        self.response_headers = response.headers
        if response.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')
        return super().__init__(json.loads(response.text))
