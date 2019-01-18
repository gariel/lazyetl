
from steps import executionStep
from xxml import Xml, XmlNode


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

@executionStep(
    input={"xml": Xml, "xPath": str},
    output={"node": XmlNode})
class XmlNodesStep:
    def execute(self):
        self.node = self.xml.get_nodes(self.xPath)