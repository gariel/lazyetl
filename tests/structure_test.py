from unittest import TestCase

import structure

class StructureTest(TestCase):
    def test_should_add_all_classes_to_xml_serializator(self):
        xs = structure.JobSerializator()
        
        classes = list(xs.classes.keys()) + ["jobserializator", "xmlserializator"]
        defined = [d.lower() for d in dir(structure) if not d.startswith("_")]

        for d in defined:
            self.assertTrue(d in classes, d + " is not in classes: " + ", ".join(classes))
