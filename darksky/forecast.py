# forecast.py
from __future__ import print_function
from builtins import super

import json
import sys
import requests

from .data import DataPoint

_API_URL = 'https://api.darksky.net/forecast'


class Forecast(DataPoint):
    def __init__(self, key, latitude, longitude, time=None, **queries):
        self._parameters = dict(key=key, latitude=latitude, longitude=longitude, time=time)
        self.refresh(**queries)

    def __setattr__(self, key, value):
        if key in ('_queries', '_parameters', '_data'):
            return object.__setattr__(self, key, value)
        return super().__setattr__(key, value)

    def __getattr__(self, key):
        if key in self.currently._data.keys():
            return self.currently._data[key]
        return object.__getattribute__(self, key)

    @property
    def url(self):
        time = self._parameters['time']
        timestr = ',{}'.format(time) if time else ''
        return '{url}/{key}/{latitude},{longitude}{timestr}'.format(url=_API_URL, timestr=timestr, **self._parameters)

    def refresh(self, **queries):
        self._queries = queries
        http_compression = {'Accept-Encoding': 'gzip'}
        request_params = {'params': self._queries, 'headers': http_compression}

        try:
            response = requests.get(self.url, **request_params)
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
