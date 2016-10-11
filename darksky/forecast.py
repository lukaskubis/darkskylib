from builtins import dict
from builtins import super
from builtins import str

import json
import sys
import requests

from .data import Data_point


class Forecast(Data_point):
    def __init__(self, api_key, latitude, longitude, **params):
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_key
        self.params = params
        self.refresh()

    def __setattr__(self, key, value):
        return object.__setattr__(self, key, value)

    def __getattr__(self, key):
        if key in self()['currently'].keys():
            return self()['currently'][key]
        return object.__getattribute__(self, key)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        del self

    @property
    def url(self):
        # insert mandatory variables
        key, lat, lng = (self.api_key, str(self.latitude), str(self.longitude))
        url = 'https://api.darksky.net/forecast/' + key + '/' + lat + ',' + lng
        if not self.params:
            return url

        # time machine request
        if 'time' in self.params.keys():
            url += ',' + str(self.params.pop('time'))

        # add optional query parameters
        url += '?'
        for key, value in self.params.items():
            url += key + '=' + str(value) + '&'
        return url

    def refresh(self, params=None, **kwparams):
        # replace current params with new ones
        if params is not None:
            self.params = params

        # update optional request parameters (if any)
        self.params = dict(self.params, **kwparams)

        # overwrite basic mandatory attributes with new values if provided
        self.api_key = self.params.pop('api_key', self.api_key)
        self.latitude = self.params.pop('latitude', self.latitude)
        self.longitude = self.params.pop('longitude', self.longitude)

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
        if response.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')

        return super().__init__(json.loads(response.text))
