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
