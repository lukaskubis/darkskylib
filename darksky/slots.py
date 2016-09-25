forecast_slots = ['_data',
                  'api_key',
                  '_options',
                  'latitude',
                  'longitude',
                  'timezone',
                  'offset',
                  'currently',
                  'minutely',
                  'hourly',
                  'daily',
                  'alerts',
                  'flags'
                  ]

data_point_slots = ['_data',
                    'time',
                    'summary',
                    'icon',
                    'sunriseTime',
                    'sunsetTime',
                    'moonPhase',
                    'nearestStormDistance',
                    'nearestStormBearing',
                    'precipIntensity',
                    'precipIntensityMax',
                    'precipIntensityMaxTime',
                    'precipProbability',
                    'precipType',
                    'precipAccumulation',
                    'temperature',
                    'temperatureMin',
                    'temperatureMinTime',
                    'temperatureMax',
                    'temperatureMaxTime',
                    'apparentTemperature',
                    'apparentTemperatureMin',
                    'apparentTemperatureMinTime',
                    'apparentTemperatureMax',
                    'apparentTemperatureMaxTime',
                    'dewPoint',
                    'windSpeed',
                    'windBearing',
                    'cloudCover',
                    'humidity',
                    'pressure',
                    'visibility',
                    'ozone'
                    ]

data_block_slots = ['summary',
                    'icon',
                    'data'
                    ]

flags_slots = ['darksky_unavailable',
               'darksky_stations',
               'datapoint_stations',
               'lamp_stations',
               'isd_stations',
               'madis_stations',
               'metar_stations',
               'metno_license',
               'sources',
               'units'
               ]

alerts_slots = ['title',
                'expires',
                'description',
                'uri'
                ]
