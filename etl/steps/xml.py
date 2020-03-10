from etl.common import StepController
from etl.libraries import xxml


class Xml(StepController):
    def from_string(self, text: str) -> xxml.Xml:
        xml = xxml.Xml()
        xml.loads(text)
        return xml

    def to_string(self, xml: xxml.Xml) -> str:
        return str(xml)

    def get_value(self, xml: xxml.Xml, xpath: str) -> str:
        return xml.get_str(xpath)
