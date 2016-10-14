# darkskylib
[![Build Status](https://travis-ci.org/lukaskubis/darkskylib.svg?branch=master)](https://travis-ci.org/lukaskubis/darkskylib) [![GitHub release](https://img.shields.io/github/release/lukaskubis/darkskylib.svg)](https://github.com/lukaskubis/darkskylib/releases) [![PyPI](https://img.shields.io/pypi/v/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![PyPI](https://img.shields.io/pypi/status/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![python](https://img.shields.io/pypi/pyversions/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![GitHub license](https://img.shields.io/badge/license-MIT-lightgray.svg)](https://raw.githubusercontent.com/lukaskubis/darkskylib/master/LICENSE)

This Python library for the [Dark Sky API](https://darksky.net/dev/docs) provides access to detailed weather information from around the globe.


* [Quick start](#quick-start)
  * [Installation](#installation)
  * [API Calls](#api-calls)
  * [Data Points and Data Blocks](#data-points-and-data-blocks)
  * [Flags and Alerts](#flags-and-alerts)
  * [Updating data](#updating-data)
* [TODOs](#todos-before-v03-beta)
* [License](#license)

## Quick start
Before you start using this library, you need to get your API key [here](https://darksky.net/dev/register).

### Installation

    pip install darkskylib

### API Calls
There are more ways to access the API data. Function `forecast` handles all request parameters and returns a `Forecast` object.

```python
>>> from darksky import forecast
>>> boston = forecast(key, 42.3601, -71.0589)
>>>
```

The first 3 positional arguments are identical to the 3 required parameters for API call. The optional query parameters need to be provided as keyword arguments. You can optionally use a dictionary with corresponding names and values. Providing additional keyword arguments in this instance will update the corresponding values in the dictionary. You can also provide all parameters using keyword arguments only.

```python
>>> boston_settings = {'key':key, 'latitude':42.3601, 'longitude':-71.0589}
>>> boston = forecast(boston_settings)
>>>
```

If you don't know the latitude and longitude of the location, you can replace them with a search query string as a second positional argument.
I do not include the required geopy library in a list of dependencies since this feature is beyond the API, however, I might add it in the future.
If you don't have geopy installed, exception is raised.

Also, at this moment, this is the only configuration of 2 arguments that works:

```python
>>> boston = forecast(key, 'Boston')
>>>
```

Using `time` argument will get you a **time machine call**.

```python
>>> from datetime import datetime as dt
>>> t = dt(2013, 5, 6, 12).isoformat()
>>> boston = forecast(settings, time=t)
>>> boston.time
1367866800
```

### Data Points and Data Blocks
The values are accessed using instance attributes. You can access current values directly, without going through `currently` data point.

```python
>>> boston.temperature
60.72
```

**Data blocks** are indexable and iterable, simply use `boston.hourly[index]` to access the data.

```python
>>> len(boston.hourly)
24
>>>
>>> boston.hourly[1].temperature
59.49
>>>
>>> # list temperatures for next 10 hours using slicing
... [hour.temperature for hour in boston.hourly[:10]]
[60.83, 59.49, 58.93, 57.95, 56.01, 53.95, 51.21, 49.21, 47.95, 46.31]
```

### Flags and Alerts
All `-` symbols in attribute names of **Flags** objects are replaced by `_` symbols. This doesn't affect the keys in raw data dictionary, but it's a necessary change that needs to be done in order to keep the functionality consistent throughout the library.

```python
>>> # instead of 'boston.flags.isd-stations'
... boston.flags.isd_stations
['383340-99999', '383390-99999', '383410-99999', '384620-99999', '384710-99999']
```

Even though **Alerts** are represented by a list, the data accessibility through instance attributes is preserved for alerts in the list.

```python
... boston.alerts[0].description
'Flood Watch for Mason, WA'
```

### Raw data
Call any object as a function to get its raw data:

```python
>>> boston.currently()
{'nearestStormBearing': 42, 'temperature': 60.72, 'nearestStormDistance': 13, 'pressure': 1020.49, 'windBearing': 256, 'dewPoint': 53.32, 'cloudCover': 0.37, 'apparentTemperature': 60.72, 'precipProbability': 0, 'summary': 'Partly Cloudy', 'icon': 'partly-cloudy-night', 'humidity': 0.77, 'ozone': 289.05, 'precipIntensity': 0, 'windSpeed': 5.66, 'visibility': 9.62, 'time': 1476403500}
```

Calling **data block** with index number will return raw data of a **data point** specified by the index number this is equivalent to `forecast.datablock[index]()`.

```python
>>> boston.hourly(2)
{'ozone': 290.06, 'temperature': 58.93, 'pressure': 1017.8, 'windBearing': 274, 'dewPoint': 52.58, 'cloudCover': 0.29, 'apparentTemperature': 58.93, 'windSpeed': 7.96, 'summary': 'Partly Cloudy', 'icon': 'partly-cloudy-night', 'humidity': 0.79, 'precipProbability': 0, 'precipIntensity': 0, 'visibility': 8.67, 'time': 1476410400}
```
### Updating data
Use `refresh()` method to update data of a `Forecast` object. You can update any request parameter using a dictionary or keyword arguments. The `refresh()` method takes either a dictionary as a positional argument, keyword arguments or a combination of both. (disabling optional queries will be added in the next commit)

```python
>>> boston.refresh()
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476403500, 60.72, 49)

>>> settings = dict(units='si', extend='hourly')
>>> boston.refresh(settings)
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476404205, 15.81, 169)

>>> boston.refresh(units='us')
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476404489, 60.57, 169)
```

### Things useful for Developers
Response headers are stored in a dictionary under `response_headers` attribute.

```python
>>> boston.response_headers['X-response-Time']
'146.035ms'
```

## TODOs before v0.3 Beta
[![Issues](https://img.shields.io/github/issues/lukaskubis/darkskylib.svg)](https://github.com/lukaskubis/darkskylib/issues)
- [ ] docs & docstrings
- [ ] unit tests
- [x] ~~implement geocoding for location query strings~~
- [ ] implement parting human-readable strings as a `time` parameter.
- [ ] improve refreshing of mandatory parameters
- [x] ~~improve handling forecast attributes when setting values~~
- [ ] implement `__slots__` again maybe?

## License
The code is available under terms of [MIT License](https://raw.githubusercontent.com/lukaskubis/darkskylib/master/LICENSE)
