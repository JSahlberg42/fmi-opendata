# python3

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
import argparse
from datetime import timedelta
import dateutil.parser


class Observation:
    def __init__(self, locType, locId, deltaHours = 0):
        ns = {
            "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0",
            "gml": "http://www.opengis.net/gml/3.2",
            "wfs": "http://www.opengis.net/wfs/2.0" }
        wfs20 = WebFeatureService(
            url='https://opendata.fmi.fi/wfs?request=GetCapabilities',
            version='2.0.0'
        )
        try:
            resp = wfs20.getfeature(
                storedQueryID='fmi::observations::weather::simple',
                storedQueryParams={locType:  locId }
            )
        except:
            print("Error fetching data. Perhaps place is not known.")
            quit()
        resp_xml = resp.read().decode("utf-8")
        root = ET.fromstring(resp_xml)
        self.loctype = locType
        self.locid = locId
        lastTimestamp = root.findall(".//BsWfs:Time", ns)[-1].text
        self.timestamp = lastTimestamp
        self.pos = root.find(".//gml:pos", ns).text
        self.parameter = {}
        self.parameterDelta = {}
        for BsWfsElement in root.findall("./wfs:member/BsWfs:BsWfsElement/[BsWfs:Time='" + lastTimestamp + "']", ns):
            self.parameter[BsWfsElement.findall(".//BsWfs:ParameterName", ns)[0].text] = BsWfsElement.findall(".//BsWfs:ParameterValue", ns)[0].text
        if deltaHours != 0:
            self.deltaHours = deltaHours
            dtLastTimestamp = dateutil.parser.isoparse(lastTimestamp)
            dtDelta = timedelta(hours=deltaHours)
            dtdeltaTimestamp = dtLastTimestamp - dtDelta
            self.deltaTimestamp = dtdeltaTimestamp.strftime("%Y-%m-%dT%H:%M:%S") + 'Z'
            for BsWfsElement in root.findall("./wfs:member/BsWfs:BsWfsElement/[BsWfs:Time='" + self.deltaTimestamp + "']", ns):
                self.parameterDelta[BsWfsElement.findall(".//BsWfs:ParameterName", ns)[0].text] = BsWfsElement.findall(".//BsWfs:ParameterValue", ns)[0].text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loctype", default='place', choices=['place', 'fmisid', 'wmo'])
    parser.add_argument("locid")
    parser.add_argument("--delta", type=int, default=0)
    args = parser.parse_args()
    if args.delta > 11:
        print("delta is too high, use 1 to 11")
        exit(42)
    obs = Observation(args.loctype, args.locid, args.delta)
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
