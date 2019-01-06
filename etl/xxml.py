
import re
import io
import xml.etree.ElementTree as ET

class Serializator:
    def __init__(self):
        self.classes = {}

    def add_class(self, clazz):
        self.classes[clazz.__name__.lower()] = clazz

    def serialize(self, obj):
        xml = Xml()
        xml.name = type(obj).__name__.lower()
        self._serialize_internal(xml, obj)
        return xml

    def deserialize(self, xml):
        if isinstance(xml, str):
            xmltmp = Xml()
            xmltmp.loads(xml)
        elif not isinstance(xml, XmlNode):
            raise Exception("Invalid type for deserialize: " + str(type(xml)))
        else:
            xmltmp = xml

        return self._deserialize_internal(xmltmp)


    def _serialize_internal(self, node, obj):
        d = obj.__dict__
        for k, v in d.items():
            t = type(v)
            if t == list:
                child_list = node.create_node(k)
                for c in v:
                    tchild = type(c)
                    child = child_list.create_node(tchild.__name__.lower())
                    self._serialize_internal(child, c)
            elif t == str:
                node.create_node(k, str(v))
            else:
                child = node.create_node(k)
                self._serialize_internal(child, v)

    def _deserialize_internal(self, node):
        obj = self.classes[node.name]()
        fields = dir(obj)
        for childnode in node.children:
            cname = childnode.name
            if cname not in fields:
                raise Exception("Invalid child for object on deserialization: " 
                    + cname + " in " + node.name)

            orig = getattr(obj, cname)
            if isinstance(orig, list):
                setattr(obj, cname, [self._deserialize_internal(childnode2) 
                    for childnode2 in childnode.children])
            elif isinstance(orig, str):
                setattr(obj, cname, childnode.value)
            else:
                setattr(obj, cname, self._deserialize_internal(childnode))
        return obj


class XmlNode:
    def __init__(self, item):
        self.item = item

    def get_name(self):
        return self.item.tag
    def set_name(self, name):
        self.item.tag = name
    name = property(get_name, set_name)

    def get_value(self):
        return self.item.text
    def set_value(self, value):
        self.item.text = value
    value = property(get_value, set_value)

    def get_children(self):
        return [XmlNode(c) for c in self.item.getchildren()]
    children = property(get_children)

    def get_attributes(self):
        return self.item.attrib
    attributes = property(get_attributes)

    def get_nodes(self, xPath): 
        return [XmlNode(i) for i in self.item.findall(xPath)]

    def get_node(self, xPath):
        r = self.item.find(xPath)
        if r is not None:
            return XmlNode(r)

    def _get(self, xPath, type):
        node = self.getNode(xPath)
        if node:
            return type(node.value())
        return type()

    def get_str(self, xPath): 
        return self._get(xPath, str)

    def get_int(self, xPath): 
        return self._get(xPath, int)

    def get_float(self, xPath): 
        return self._get(xPath, float)

    def create_node(self, name, value=None):
        e = ET.SubElement(self.item, name)
        if (value):
            e.text = value
        return XmlNode(e)

    def remove_node(self, xPath):
        e = root.find(xPath)
        self.item.remove(e)

    def dynamic(self):
        return XmlDynamic(self)

    def __str__(self):
        return ET.tostring(self.item, encoding='utf8').decode('utf8')


class Xml(XmlNode):
    def __init__(self):
        super().__init__(ET.Element('root'))

    def load(self, filename, encoding='utf-8'):
        with io.open(filename, 'r', encoding=encoding) as f:
            self.loads(f.read())

    def loads(self, text):
        self.item = ET.fromstring(self._removerNS(text))

    def _removerNS(self, text):
        noNS = re.sub(r"xmlns:?[^=]*=([\"][^\"]*[\"])|(xmlns:?[^=]*=['][^']*['])", "", text);
        noNSOpenTag = re.sub(r"<\w*:", "<", noNS);
        noNSCloseTag = re.sub(r"</\w*:", "</", noNSOpenTag);
        return noNSCloseTag


class XmlDynamic(object):
    def __init__(self, node):
        self._node = node

    def many(self, pattern):
        return [Xml(xml=None, element=ee) for ee in self._node.item.ChildNodes if re.match(pattern, ee.Name)]

    def __str__(self):
        return self.Value

    def __call__(self):
        return self.Value

    def __exists(self):
        return self._node is not None
    _exists = property(__exists)

    def __name(self):
        return self._node.item.Name
    _name = property(__name)

    def __value(self):
        e = self._node
        return e and e.item.text
    
    def __getattribute__(self, name):
        if name.startswith("_") or name in dir(self):
            return object.__getattribute__(self, name)
        return Xml2(e.getNode(name));
