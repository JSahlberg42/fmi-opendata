# python3

from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET


class Observation:
    def __init__(self, icaocode):
        wfs20 = WebFeatureService(url='https://opendata.fmi.fi/wfs?request=GetCapabilities', version='2.0.0')
        resp = wfs20.getfeature(storedQueryID='fmi::avi::observations::latest::iwxxm', storedQueryParams={'icaocode':  icaocode })
        resp_xml = resp.read().decode("utf-8")
        root = ET.fromstring(resp_xml)
        self.icaocode = icaocode
        self.phenomenonTime = root.findall(".//{http://www.opengis.net/gml/3.2}timePosition")[0].text
        self.airTemperature = root.findall(".//{http://icao.int/iwxxm/1.0}airTemperature")[0].text
        self.dewpointTemperature = root.findall(".//{http://icao.int/iwxxm/1.0}dewpointTemperature")[0].text
        self.qnh = root.findall(".//{http://icao.int/iwxxm/1.0}qnh")[0].text
        self.meanWindDirection = root.findall(".//{http://icao.int/iwxxm/1.0}meanWindDirection")[0].text
        self.meanWindSpeed = root.findall(".//{http://icao.int/iwxxm/1.0}meanWindSpeed")[0].text

def main():
    efhk = Observation('EFHK')
    print("EFHK weather at", efhk.phenomenonTime)
    print("Air temperature:", efhk.airTemperature, "C")
    print("Dewpoint:", efhk.dewpointTemperature, "C")
    print("Airpressue:", efhk.qnh, "hPa")
    print("Wind Direction (mean):", efhk.meanWindDirection, "degrees")
    print("Wind Speed (mean):", efhk.meanWindSpeed, "m/s")

if __name__ == "__main__":
    main()
