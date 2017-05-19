# forecast.py

from builtins import super

import json
import sys
import requests

from .data import DataPoint
class Forecast(DataPoint):
    def __init__(self, key, latitude, longitude, **queries):
        self._parameters = dict(key=key, latitude=latitude, longitude=longitude)
        self.refresh(**queries)

    def __setattr__(self, key, value):
        if key in ('_queries', '_parameters', '_data'):
            return object.__setattr__(self, key, value)
        return super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.currently._data.keys():
            return self.currently._data[key]
        return object.__getattribute__(self, key)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        del self

    @property
    def url(self):
        # insert mandatory variables
        url = 'https://api.darksky.net/forecast/'
        url += self._parameters['key'] + '/'
        url += str(self._parameters['latitude']) + ','
        url += str(self._parameters['longitude'])
        if not self._queries:
            return url

        # time machine
        if 'time' in self._queries.keys():
            url += ',' + str(self._queries['time'])

        # add optional query parameters
        url += '?'
        for key, value in self._queries.items():
            url += key + '=' + str(value) + '&'
        return url


    def refresh(self, **queries):
        # update query parameters
        self._queries = queries

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
