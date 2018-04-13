import os
import pickle
import unittest

import darksky


class TestPickle(unittest.TestCase):
    """ Forecast pickling """
    @classmethod
    def setUpClass(cls):
        cls.key = os.environ['DARKSKY_KEY']

    @classmethod
    def tearDownClass(cls):
        os.system('find . -name "*.pickle" -exec rm {} \;')

    def test_pickle(self):
        forecast = darksky.forecast(self.key, -77.843906, 166.686520)
        with open('./forecast.pickle', 'wb') as outfile:
            pickle.dump(forecast, outfile)

        self.assertTrue(os.path.exists('./forecast.pickle'))

    def test_unpickle(self):
        self.assertTrue(os.path.exists('./forecast.pickle'))

        with open('./forecast.pickle', 'rb') as infile:
            forecast = pickle.load(infile)

        self.assertTrue(forecast)


if __name__ == '__main__':
    unittest.main()
