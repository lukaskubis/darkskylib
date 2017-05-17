# darkskylib
[![GitHub release](https://img.shields.io/github/release/lukaskubis/darkskylib.svg)](https://github.com/lukaskubis/darkskylib/releases) [![PyPI](https://img.shields.io/pypi/v/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![PyPI](https://img.shields.io/pypi/status/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![python](https://img.shields.io/pypi/pyversions/darkskylib.svg)](https://pypi.python.org/pypi/darkskylib) [![GitHub license](https://img.shields.io/badge/license-MIT-lightgray.svg)](https://raw.githubusercontent.com/lukaskubis/darkskylib/master/LICENSE)

This Python library for the [Dark Sky API](https://darksky.net/dev/docs) provides access to detailed weather information from around the globe.


* [Installation](#installation)
* [API Calls](#api-calls)
* [Data Points and Data Blocks](#data-points-and-data-blocks)
* [Flags and Alerts](#flags-and-alerts)
* [Updating data](#updating-data)
* [Developer utilities](#things-useful-for-developers)
* [Example Script](#example-script)
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

The first 3 positional arguments are identical to the 3 required parameters for API call. The optional query parameters need to be provided as keyword arguments.

Using `time` argument will get you a **time machine call**.

```python
>>> BOSTON = key, 42.3601, -71.0589
>>> from datetime import datetime as dt
>>> t = dt(2013, 5, 6, 12).isoformat()
>>> boston = forecast(*BOSTON, time=t)
>>> boston.time
1367866800
```

### Data Points and Data Blocks
The values are accessed using instance attributes. You can access current values directly, without going through `currently` data point.

```python
>>> boston.temperature
60.72
```

**Data blocks** are indexable and iterable by their data.

```python
>>> len(boston.hourly)
24
>>>
>>> boston.hourly[1].temperature
59.49
>>>
>>> # list temperatures for next 10 hours
... [hour.temperature for hour in boston.hourly[:10]]
[60.83, 59.49, 58.93, 57.95, 56.01, 53.95, 51.21, 49.21, 47.95, 46.31]
```

### Flags and Alerts
All dashes `-` in attribute names of **Flags** objects are replaced by underscores `_`. This doesn't affect the keys in raw data dictionary, but it's a necessary change in order to keep the functionality consistent throughout the library.

```python
>>> # instead of 'boston.flags.isd-stations'
... boston.flags.isd_stations
['383340-99999', '383390-99999', '383410-99999', '384620-99999', '384710-99999']
```

Even though **Alerts** are represented by a list, the data accessibility through instance attributes is preserved for alerts in the list.

```python
>>> boston.alerts[0].title
'Freeze Watch for Norfolk, MA'
```

### Raw data
Use `rawdata` attribute:

```python
>>> boston.hourly[2].rawdata
{'ozone': 290.06, 'temperature': 58.93, 'pressure': 1017.8, 'windBearing': 274, 'dewPoint': 52.58, 'cloudCover': 0.29, 'apparentTemperature': 58.93, 'windSpeed': 7.96, 'summary': 'Partly Cloudy', 'icon': 'partly-cloudy-night', 'humidity': 0.79, 'precipProbability': 0, 'precipIntensity': 0, 'visibility': 8.67, 'time': 1476410400}
```

### Updating data
Use `refresh()` method to update data of a `Forecast` object. The `refresh()` method takes optional queries (including `time`, making it a **Time machine** object) as keyword arguments. Calling `refresh()` without any arguments will set all queries to default values.

```python
>>> boston.refresh()
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476403500, 60.72, 49)
>>>
>>> settings = dict(units='si', extend='hourly')
>>> boston.refresh(settings)
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476404205, 15.81, 169)
>>>
>>> boston.refresh(units='us')
>>> (boston.time, boston.temperature, len(boston.hourly))
(1476404489, 60.57, 49)
```

### For Developers
Response headers are stored in a dictionary under `response_headers` attribute.

```python
>>> boston.response_headers['X-response-Time']
'146.035ms'
```

## Example script
```python
from darksky import forecast
from datetime import date, timedelta

BOSTON = 42.3601, 71.0589

weekday = date.today()
with forecast('API_KEY', *BOSTON) as boston:
    print(boston.daily.summary, end='\n---\n')
    for day in boston.daily:
        day = dict(day = date.strftime(weekday, '%a'),
                   sum = day.summary,
                   tempMin = day.temperatureMin,
                   tempMax = day.temperatureMax
                   )
        print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
        weekday += timedelta(days=1)
```
Output:

    Light rain on Friday and Saturday, with temperatures bottoming out at 48°F on Tuesday.
    ---
    Sun: Partly cloudy in the morning. Temp range: 44.86 - 57.26°F
    Mon: Mostly cloudy in the morning. Temp range: 44.26 - 55.28°F
    Tue: Clear throughout the day. Temp range: 36.85 - 47.9°F
    Wed: Partly cloudy starting in the afternoon, continuing until evening. Temp range: 33.23 - 47.93°F
    Thu: Light rain overnight. Temp range: 35.75 - 49.71°F
    Fri: Light rain in the morning and afternoon. Temp range: 45.47 - 57.11°F
    Sat: Drizzle in the morning. Temp range: 43.3 - 62.08°F
    Sun: Clear throughout the day. Temp range: 39.81 - 60.84°F

## License
The code is available under terms of [MIT License](https://raw.githubusercontent.com/lukaskubis/darkskylib/master/LICENSE)
