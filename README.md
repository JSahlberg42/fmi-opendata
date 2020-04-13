# fmi-opendata

## FmiObsWeatherSimple
Example
```
from fmiOpendata import FmiObsWeatherSimple

obs = FmiObsWeatherSimple('place', 'Helsinki') # FmiObsWeatherSimple(locType, locId, deltaHours = 0)

for key in obs.parameter.keys():
    print(key, obs.parameter[key])
```

see weatherObervationHelsinki.py as example

locType and locId must be defined.
locType values and example values for locId:
* place (Helsinki)
* fmisid (151028, https://www.ilmatieteenlaitos.fi/havaintoasemat)
* wmo (02701, https://www.ilmatieteenlaitos.fi/havaintoasemat)

deltaHours is optional. Values can be between 1 and 11. If defined, it returns past parameter values in parameterDelta dictionary.

| variable | type | description |
| --- | --- | --- |
locid | str | location ID
loctype | str | location ID type
parameter | dict | fetched params and values
parameterDelta | dict | fetched historial params and values
pos | str | observation spot location (EUREF-FIN)
timestamp | str | observation timestamp, format '2020-04-13T07:50:00Z'
