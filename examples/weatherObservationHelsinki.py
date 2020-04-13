from fmiOpendata import FmiObsWeatherSimple

obs = FmiObsWeatherSimple('place', 'Helsinki')

for key in obs.parameter.keys():
    print(key, obs.parameter[key])
