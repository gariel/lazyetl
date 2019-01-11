
from steps import executionStep
from xxml import Xml


@executionStep(
    input={"text": str},
    output={"xml": Xml})
class TextToXmlStep:
    def execute(self):
        self.xml = Xml()
        self.xml.loads(self.text)

@executionStep(
    input={"xml": Xml},
    output={"text": str})
class XmlToTextStep:
    def execute(self):
        self.text = str(self.xml)

@executionStep(
    input={"xml": Xml, "xPath": str},
    output={"value": str})
class GetXmlFieldValueStep:
    def execute(self):
        self.value = self.xml.get_str(self.xPath)