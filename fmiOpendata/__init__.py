# python3

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
from datetime import timedelta
import dateutil.parser


class FmiObsWeatherSimple:
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
    pass

if __name__ == "__main__":
    main()
