# python3
from fmiOpendata import FmiObsWeatherSimple
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loctype", default='place', choices=['place', 'fmisid', 'wmo'])
    parser.add_argument("locid")
    parser.add_argument("--delta", type=int, default=0)
    args = parser.parse_args()
    if args.delta > 11:
        print("delta is too high, use 1 to 11")
        exit(42)
    obs = FmiObsWeatherSimple(args.loctype, args.locid, args.delta)
    print("Weather at", obs.locid, "(loctype: " + obs.loctype + ") pos: " + obs.pos)
    if len(obs.parameterDelta.keys()) > 0:
        print(obs.deltaTimestamp)
        for key in obs.parameterDelta.keys():
            if obs.parameterDelta[key] != 'NaN':
                print(key, obs.parameterDelta[key])
    print(obs.timestamp)
    for key in obs.parameter.keys():
        if obs.parameter[key] != 'NaN':
            print(key, obs.parameter[key])


if __name__ == "__main__":
    main()
