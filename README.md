# forepycast
[![Build Status](https://travis-ci.org/lukaskubis/forepycast.svg?branch=master)](https://travis-ci.org/lukaskubis/forepycast) [![GitHub release](https://img.shields.io/github/release/lukaskubis/forepycast.svg)](https://github.com/lukaskubis/forepycast/releases) [![PyPI](https://img.shields.io/pypi/v/forepycast.svg)](https://pypi.python.org/pypi/forepycast) [![PyPI](https://img.shields.io/pypi/status/forepycast.svg)](https://pypi.python.org/pypi/forepycast) [![python](https://img.shields.io/pypi/pyversions/forepycast.svg)](https://pypi.python.org/pypi/forepycast) [![GitHub license](https://img.shields.io/badge/license-MIT-lightgray.svg)](https://raw.githubusercontent.com/lukaskubis/forepycastio/master/LICENSE)

![In action](http://i.imgur.com/XfJ82jV.gif)

Python wrapper for the [The Dark Sky Forecast API](https://developer.forecast.io/docs/v2). This library provides access to detailed weather information from around the globe.

* [Quick start](#quick-start)
  * [Installation](#installation)
  * [API Calls](#api-calls)
  * [Data Points and Data Blocks](#data-points-and-data-blocks)
  * [Flags and Alerts](#flags-and-alerts)
  * [Updating data](#updating-data)
* [TODOs](#todos-before-v02)
* [License](#license)

## Quick start
Before you start using this library, you need to get your API key [here](https://developer.forecast.io).

### Installation

    pip install forepycast

From [PyPI](https://pypi.python.org/pypi/forepycast/)

    python setup.py install


### API Calls
There are more ways to access the API data. Function `forecast` handles all request parameters passed either by dictionary, keyword arguments, or combination of both. Returns a `Forecast` object. Keyword arguments are useful when some of the values from dictionary are not correct. An alternative to this would be using the `Forecast` object directly, which takes the 3 mandatory request parameters as positional arguments.

```python
>>> from forepycast import forecast
>>> settings = {'api_key':key, 'latitude':37.826833, 'longitude':-122.423186, 'units':'si'}
>>> alcatraz = forecast(settings, units='us')
>>> alcatraz.flags.units
us
```

Using `time` argument will get you a **time machine call**.

```python
>>> from datetime import datetime as dt
>>> t = dt(2013, 5, 6, 12).isoformat()
>>> alcatraz = forecast(settings, time=t)
>>> alcatraz.time
1367866800
```

### Data Points and Data Blocks
The values are accessed using instance attributes. You can access current values directly.

```python
>>> alcatraz.temperature
17.14
```

**Data blocks** are indexable and iterable, simply use `alcatraz.hourly[index]` to access the data.

```python
>>> len(alcatraz.hourly)
24

>>> alcatraz.hourly[1].temperature
14.16

>>> # list temperatures for next 10 hours using slicing
... [hour.temperature for hour in alcatraz.hourly[:10]]
[14.6, 14.16, 14.57, 14.37, 14.37, 14.37, 14.57, 14.48, 15.39, 16.35]
```

### Flags and Alerts
All `-` symbols in attribute names of **Flags** objects are replaced by `_` symbols. This doesn't affect the keys in raw data dictionary.

```python
>>> alcatraz.flags.isd_stations
['994016-99999', '998197-99999', '998476-99999', '998479-99999', '999999-23272']
```

The functionality of **Alerts** hasn't been tested yet

### Raw data
Call any object as a function to get its raw data:

```python
>>> alcatraz.currently()
{'windSpeed': 1.63, 'summary': 'Clear', 'pressure': 1011.72, 'time': 1367866800, 'apparentTemperature': 17.14, 'temperature': 17.14, 'precipType': 'rain', 'windBearing': 197, 'icon': 'clear-day'}
```

A **data block** called with index will return raw data of a **data point** specified by the index number.

```python
>>> alcatraz.hourly(2)
{'windSpeed': 2.53, 'summary': 'Clear', 'pressure': 1009.99, 'time': 1367830800, 'apparentTemperature': 14.57, 'temperature': 14.57, 'precipType': 'rain', 'windBearing': 17, 'icon': 'clear-night'}
```
### Updating data
Use `refresh` method to update data of a `Forecast` object. You can update any request parameter (including *api_key*, *latitude* and *longitude* although, if once changed, they cannot be set to their original state implicitly right now) using a dictionary or keyword arguments. To disable an optional query parameter (make it default) set the attribute to `None`. Using empty dictionary will reset all optional parameters to their default values (and get rid of **time machine** as well). Note that `time` parameter gets reset every time, unless given as argument (this is a feature).

```python
>>> alcatraz.refresh()
>>> (alcatraz.time, alcatraz.temperature, len(alcatraz.hourly))
(1473164637, 12.62, 49)

>>> settings = {'time':t, 'units':'us'}
>>> alcatraz.refresh(settings)
>>> (alcatraz.time, alcatraz.temperature, len(alcatraz.hourly))
(1367866800, 62.86, 24)

>>> alcatraz.refresh(extend='hourly')
>>> (alcatraz.time, alcatraz.temperature, len(alcatraz.hourly))
(1473164741, 54.7, 169)

>>> alcatraz.refresh({})
>>> (alcatraz.time, alcatraz.temperature, len(alcatraz.hourly))
(1473164785, 54.69, 49)
```
## TODOs before v0.3 Beta
[![Issues](https://img.shields.io/github/issues/lukaskubis/forepycast.svg)](https://github.com/lukaskubis/forepycast/issues)
- [ ] docs & docstrings
- [ ] unit tests
- [x] ~~improve refreshing of mandatory parameters~~
- [x] ~~improve handling forecast attributes when setting values~~

## License
The code is available under terms of [MIT License](https://raw.githubusercontent.com/lukaskubis/forepycastio/master/LICENSE)
