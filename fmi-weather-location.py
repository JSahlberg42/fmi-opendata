# python3

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
import argparse


class Observation:
    def __init__(self, place):
        ns = {
            "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0",
            "gml": "http://www.opengis.net/gml/3.2",
            "wfs": "http://www.opengis.net/wfs/2.0" }
        wfs20 = WebFeatureService(url='https://opendata.fmi.fi/wfs?request=GetCapabilities', version='2.0.0')
        try:
            resp = wfs20.getfeature(storedQueryID='fmi::observations::weather::simple', storedQueryParams={'place':  place })
        except:
            print("error.")
            quit()
        resp_xml = resp.read().decode("utf-8")
        root = ET.fromstring(resp_xml)
        self.place = place
        lastTimestamp = root.findall(".//BsWfs:Time", ns)[-1].text
        self.timestamp = lastTimestamp
        self.pos = root.find(".//gml:pos", ns).text
        self.parameter = {}
#        print(self.place, self.pos, self.lastTimestamp)
        for BsWfsElement in root.findall("./wfs:member/BsWfs:BsWfsElement/[BsWfs:Time='" + lastTimestamp + "']", ns):
            self.parameter[BsWfsElement.findall(".//BsWfs:ParameterName", ns)[0].text] = BsWfsElement.findall(".//BsWfs:ParameterValue", ns)[0].text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("place")
    args = parser.parse_args()
    obs = Observation(args.place)
    print("Weather at", obs.place, obs.pos, "at", obs.timestamp)
    for key in obs.parameter.keys():
        if obs.parameter[key] != 'NaN':
            print(key, obs.parameter[key])

if __name__ == "__main__":
    main()
