
import re
import io
from typing import Type, Any, Union, List, Dict, Optional
from xml.etree import ElementTree


class XmlNode:
    def __init__(self, item):
        self.item = item

    @property
    def name(self) -> str:
        return self.item.tag

    @name.setter
    def name(self, value: str):
        self.item.tag = value

    @property
    def value(self) -> str:
        return self.item.text

    @value.setter
    def value(self, value: str):
        self.item.text = value

    @property
    def children(self) -> List["XmlNode"]:
        return [XmlNode(c) for c in self.item.getchildren()]

    @property
    def attributes(self) -> Dict[str, str]:
        return self.item.attrib

    def get_nodes(self, xpath: str) -> List["XmlNode"]:
        return [XmlNode(i) for i in self.item.findall(xpath)]

    def get_node(self, xpath: str) -> Optional["XmlNode"]:
        r = self.item.find(xpath)
        if r is not None:
            return XmlNode(r)

    def _get(self, xpath, data_type):
        node = self.get_node(xpath)
        if node and node.value:
            return data_type(node.value)
        return data_type()

    def get_str(self, xpath: str) -> str:
        return self._get(xpath, str)

    def get_int(self, xpath: str) -> int:
        return self._get(xpath, int)

    def get_float(self, xpath: str) -> float:
        return self._get(xpath, float)

    def create_node(self, name: str, value: Any = None) -> "XmlNode":
        e = ElementTree.SubElement(self.item, name)
        if value:
            e.text = value
        return XmlNode(e)

    def remove_node(self, xpath: str):
        e = self.item.find(xpath)
        parent = self.item.find(xpath + "/...")
        parent.remove(e)

    def dynamic(self):
        return XmlDynamic(self)

    def __str__(self):
        return ElementTree.tostring(self.item, encoding='utf8').decode('utf8')


class Xml(XmlNode):
    def __init__(self):
        super().__init__(ElementTree.Element('root'))

    def load(self, filename: str, encoding: str = 'utf-8'):
        with io.open(filename, 'r', encoding=encoding) as f:
            self.loads(f.read())

    def loads(self, text: str):
        self.item = ElementTree.fromstring(self._remove_namespaces(text))

    def _remove_namespaces(self, text):
        no_ns = re.sub(r"xmlns:?[^=]*=([\"][^\"]*[\"])|(xmlns:?[^=]*=['][^']*['])", "", text)
        no_ns_open_tag = re.sub(r"<\w*:", "<", no_ns)
        no_ns_close_tag = re.sub(r"</\w*:", "</", no_ns_open_tag)
        return no_ns_close_tag


class XmlSerializer:
    def __init__(self):
        self.classes = {}

    def add_type(self, clazz: Type):
        self.classes[clazz.__name__.lower()] = clazz

    def serialize(self, obj: Any) -> Xml:
        xml = Xml()
        xml.name = type(obj).__name__.lower()
        self._serialize_internal(xml, obj)
        return xml

    def deserialize(self, xml: Union[Xml, str]) -> object:
        if isinstance(xml, str):
            tmp = Xml()
            tmp.loads(xml)
        elif not isinstance(xml, XmlNode):
            raise Exception(f"Invalid type for deserialize: {type(xml)}")
        else:
            tmp = xml

        return self._deserialize_internal(tmp)

    def _serialize_internal(self, node, obj):
        d = obj.__dict__
        for k, v in d.items():
            t = type(v)
            if t == list:
                child_list = node.create_node(k)
                for c in v:
                    type_child = type(c)
                    child = child_list.create_node(type_child.__name__.lower())
                    self._serialize_internal(child, c)
            elif t == str:
                node.create_node(k, str(v))
            else:
                child = node.create_node(k)
                self._serialize_internal(child, v)

    def _deserialize_internal(self, node):
        if node.name not in self.classes:
            raise Exception(f"Type not added for deserialization: {node.name}")
        obj = self.classes[node.name]()
        fields = dir(obj)
        for child in node.children:
            cname = child.name
            if cname not in fields:
                raise Exception(f"Invalid child for object on deserialization: {cname} in {node.name}")

            orig = getattr(obj, cname)
            if isinstance(orig, list):
                setattr(obj, cname, [self._deserialize_internal(sub_child) for sub_child in child.children])
            elif isinstance(orig, str):
                setattr(obj, cname, child.value)
            else:
                setattr(obj, cname, self._deserialize_internal(child))
        return obj


class XmlDynamic(object):
    def __init__(self, node):
        self._node = node

    def _many(self, pattern=None):
        validate = None
        if pattern:
            re_many = re.compile(pattern)
            validate = re_many.match

        return [XmlDynamic(node) for node in self._node.children if not validate or validate(node.name)]

    def __str__(self):
        return self._value

    def __call__(self):
        return self._value

    def __exists(self):
        return self._node is not None
    _exists = property(__exists)

    def __name(self):
        return self._node and self._node.name
    _name = property(__name)

    def __value(self):
        return self._node and self._node.value
    _value = property(__value)

    def __getattribute__(self, name):
        if name.startswith("_") or name in dir(self):
            return object.__getattribute__(self, name)
        return XmlDynamic(self._node.get_node(name))
