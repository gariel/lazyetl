
from steps import executionStep

@executionStep(
    input={"text": str},
    output={"result": str})
class UpperCaseStep:
    def execute(self):
        self.result = self.text.upper()


@executionStep(
    input={"text": str},
    output={"result": str})
class LowerCaseStep:
    def execute(self):
        self.result = self.text.lower()
