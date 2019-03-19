import os
import pickle
import unittest

import darksky
import requests


class TestPickle(unittest.TestCase):
    """ Forecast pickling """
    @classmethod
    def setUpClass(cls):
        def mock_request_get(*args, **kwargs):
            response = type('Response', (object,), {})
            response.headers = {}
            response.status_code = 200

            with open('./test/response.json', 'r') as fixture:
                response.text = fixture.read()

            return response

        cls.request_get = requests.get
        requests.get = mock_request_get

    @classmethod
    def tearDownClass(cls):
        os.system('find . -name "*.pickle" -exec rm {} \;')
        requests.get = cls.request_get

    def test_pickle(self):
        location = -77.843906, 166.686520  # McMurdo station, antarctica

        # This doesn't actually hit the API since we mocked out the request lib
        forecast = darksky.forecast('test_key', *location)

        # Make sure we got the right data, via our mock
        self.assertEqual(forecast.currently.temperature, -23.58)

        # Ensure pickling by actually pickling
        with open('./forecast.pickle', 'wb') as outfile:
            pickle.dump(forecast, outfile)

        # Check that the file exists
        self.assertTrue(os.path.exists('./forecast.pickle'))

    def test_unpickle(self):
        # Check that the previous test, which writes out the pickle, succeeded
        self.assertTrue(os.path.exists('./forecast.pickle'))

        # Load the pickle file
        with open('./forecast.pickle', 'rb') as infile:
            forecast = pickle.load(infile)

        # Make sure it loaded right
        self.assertTrue(forecast)
        self.assertEqual(forecast.currently.temperature, -23.58)


if __name__ == '__main__':
    unittest.main()
