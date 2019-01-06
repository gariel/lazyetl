
from steps import executionStep

@executionStep(
    input={"text": str})
class PrintStep:
    def execute(self):
        print(self.text)


@executionStep(
    input={"text": str},
    output={"input": str})
class UserInputStep:
    def execute(self):
        self.input = input(self.message)
