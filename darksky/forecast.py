from builtins import dict
from builtins import super
from builtins import str

import json
import sys
import requests

from .data import Data_point


class Forecast(Data_point):
    def __init__(self, api_key, latitude, longitude, **settings):
        self.latitude = latitude
        self.longitude = longitude
        self.api_key = api_key
        self.settings = settings
        self.refresh()

    def __setattr__(self, name, value):
        if name in ('_data', 'api_key', 'settings', 'latitude', 'longitude'):
            return object.__setattr__(self, name, value)
        return super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self()['currently'].keys():
            return self()['currently'][name]
        return object.__getattribute__(self, name)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        del self

    @property
    def url(self):
        # insert mandatory variables
        key, lat, lng = (self.api_key, str(self.latitude), str(self.longitude))
        url = 'https://api.darksky.net/forecast/' + key + '/' + lat + ',' + lng
        if not self.settings:
            return url

        # time machine request
        if 'time' in self.settings.keys():
            url += ',' + self.settings.pop('time')

        # add optional query parameters
        url += '?'
        for key, value in self.settings.items():
            url += key + '=' + str(value) + '&'
        return url

    def refresh(self, settings=None, **kwsettings):
        # replace current settings with new ones
        if settings is not None:
            self.settings = settings

        # update current forecast settings (if any)
        self.settings = dict(self.settings, **kwsettings)

        # overwrite basic mandatory attributes with new values if provided
        self.api_key = self.settings.pop('api_key', self.api_key)
        self.latitude = self.settings.pop('latitude', self.latitude)
        self.longitude = self.settings.pop('longitude', self.longitude)

        # request data from API and store it in new attributes
        super().__init__(json.loads(self.request())

    def request(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.Timeout:
            print('Error: Timeout')
        except requests.exceptions.TooManyRedirects:
            print('Error: TooManyRedirects')
        except requests.exceptions.RequestException as ex:
            print(ex)
            sys.exit(1)
        try:
            cache_control = response.headers['Cache-Control']
            expires = response.headers['Expires']
            x_forecast_api_calls = response.headers['X-Forecast-API-Calls']
            x_responde_time = response.headers['X-Response-Time']
        except KeyError as kerr:
            msg = 'Warning: Could not get headers. ' + str(kerr)
            print(msg)
        if response.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')
        return response.text
