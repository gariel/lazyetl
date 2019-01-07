from unittest import TestCase
from xxml import Xml, XmlNode, XmlSerializator

xmlstr = """
<root>
    <first zxc="qwe">
        <textValue>asd</textValue>
        <numericValue>123</numericValue>
        <decimalValue>654.789</decimalValue>
    </first>
    <list>
        <item>asd</item>
        <item>qwe</item>
        <item>zxc</item>
    </list>
</root>
"""

class XmlTest(TestCase):
    def setUp(self):
        self.xml = Xml()
        self.xml.loads(xmlstr)

    def test_should_get_values_by_xPath(self):
        self.assertEqual(self.xml.get_str("first/textValue"), "asd")
        self.assertEqual(self.xml.get_int("first/numericValue"), 123)
        self.assertEqual(self.xml.get_float("first/decimalValue"), 654.789)

    def test_should_get_node_by_xPath(self):
        node = self.xml.get_node("first")
        self.assertEqual(node.get_str("textValue"), "asd")

    def test_should_get_nodes_by_xPath(self):
        result = self.xml.get_nodes("list/item")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "asd")
        self.assertEqual(result[1].value, "qwe")
        self.assertEqual(result[2].value, "zxc")

    def test_should_get_set_the_node_name(self):
        node = self.xml.get_node("first")
        self.assertEqual(node.name, "first")

        node.name = "second"
        self.assertEqual(node.name, "second")

        node2 = self.xml.get_node("second")
        self.assertIsNotNone(node2)

    def test_should_get_set_the_node_value(self):
        node = self.xml.get_node("first/numericValue")
        self.assertEqual(node.value, "123")

        node.value = "789"
        self.assertEqual(node.value, "789")

        node2 = self.xml.get_node("first/numericValue")
        self.assertEqual(node2.value, "789")

    def test_should_get_set_attribute(self):
        node = self.xml.get_node("first")
        self.assertEqual(node.attributes["zxc"], "qwe")

        node.attributes["zxc"] = "asd"
        self.assertEqual(node.attributes["zxc"], "asd")

        node.attributes["aaa"] = "bbb"
        self.assertEqual(node.attributes["aaa"], "bbb")

    def test_should_get_children_nodes(self):
        parent = self.xml.get_node("first")
        children = parent.children
        self.assertEqual(len(children), 3)
        self.assertEqual(children[0].value, "asd")
        self.assertEqual(children[1].value, "123")
        self.assertEqual(children[2].value, "654.789")

    def test_should_create_node(self):
        newNode = self.xml.create_node("newNode", "newValue")
        self.assertEqual(newNode.value, "newValue")
        self.assertEqual(self.xml.get_str("newNode"), "newValue")

    def test_should_remove_node(self):
        self.xml.remove_node("first/textValue")
        self.assertIsNone(self.xml.get_node("first/textValue"))

        self.xml.remove_node("list/item[3]")

        items = self.xml.get_nodes("list/item")
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].value, "asd")
        self.assertEqual(items[1].value, "qwe")


class XmlDynamicTest(TestCase):
    def setUp(self):
        self.xml = Xml()
        self.xml.loads(xmlstr)
        self.root = self.xml.dynamic()
    
    def test_should_get_values(self):
        self.assertEqual(self.root.first.textValue._value, "asd")
        self.assertEqual(self.root.first.textValue(), "asd")
        self.assertEqual(str(self.root.first.textValue), "asd")

    def test_should_get_names(self):
        self.assertEqual(self.root.first.textValue._name, "textValue")

    def test_should_get_values_from_list(self):
        items = self.root.list._many()
        self.assertEqual(items[0](), "asd")
        self.assertEqual(items[1](), "qwe")
        self.assertEqual(items[2](), "zxc")

    def test_should_get_values_from_list_with_regex(self):
        items = self.root.first._many(r"\w+Value")
        self.assertEqual(items[0](), "asd")
        self.assertEqual(items[1](), "123")
        self.assertEqual(items[2](), "654.789")


class SerializatorTest(TestCase):
    def setUp(self):
        self.serializator = XmlSerializator()

        class SimpleType:
            def __init__(self, a="", simpletypes=[]):
                self.a = a
                self.simpletypes = simpletypes

        self.simpletype = SimpleType
        self.serializator.add_class(SimpleType)

    def test_should_serialize_simple_type(self):
        st = self.simpletype(
            "test",
            [
                self.simpletype("sub1"),
                self.simpletype("sub2"),
                self.simpletype()
            ]
        )
        xml = self.serializator.serialize(st)
        self.assertEqual(xml.get_str("a"), "test")
        self.assertEqual(xml.get_str("simpletypes/simpletype[1]/a"), "sub1")
        self.assertEqual(xml.get_str("simpletypes/simpletype[2]/a"), "sub2")
        self.assertEqual(xml.get_str("simpletypes/simpletype[3]/a"), "")

    def test_should_deserialize_simple_type(self):
        xml = Xml()
        xml.name = "simpletype"
        xml.create_node("a", "test_deserialize")
        nodes = xml.create_node("simpletypes")
        s1 = nodes.create_node("simpletype")
        s1.create_node("a", "child1")
        s2 = nodes.create_node("simpletype")
        s2.create_node("a", "child2")

        obj = self.serializator.deserialize(str(xml))
        self.assertIsInstance(obj, self.simpletype)
        self.assertEqual(obj.a, "test_deserialize")
        self.assertEqual(len(obj.simpletypes), 2)
        self.assertEqual(obj.simpletypes[0].a, "child1")
        self.assertEqual(obj.simpletypes[1].a, "child2")

    def test_should_throw_exception_deserializing_without_classes_added(self):
        xml = Xml()
        xml.name = "simpletype"
        xml.create_node("a", "test_raise")

        nserializator = XmlSerializator()
        self.assertRaises(Exception, nserializator.deserialize, xml)
