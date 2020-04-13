from fmiOpendata import FmiObsWeatherSimple

obs = FmiObsWeatherSimple('place', 'Helsinki')

print(obs.parameter)

for key in obs.parameter.keys():
    print(key, obs.parameter[key])
