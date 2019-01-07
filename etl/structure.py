
from xxml import XmlSerializator

class Parameter:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.value = ""

class Field:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.variable = ""

class Step:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.type = ""
        self.parameters = []
        self.fields = []

class Sequence:
    def __init__(self):
        self.first = ""
        self.links = []

class Link:
    def __init__(self):
        self.idfrom = ""
        self.idto = ""

class Job:
    def __init__(self):
        self.description = ""
        self.parameters = []
        self.steps = []
        self.fields = []
        self.sequence = None

class JobSerializator(XmlSerializator):
    def __init__(self):
        super(JobSerializator, self).__init__()

        self.add_class(Parameter)
        self.add_class(Field)
        self.add_class(Step)
        self.add_class(Sequence)
        self.add_class(Link)
        self.add_class(Job)