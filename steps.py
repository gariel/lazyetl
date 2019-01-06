
class ExecutionStep:
    def execute(self):
        pass

class PrintExecutionStep(ExecutionStep):
    # in text str
    def execute(self):
        print(self.text)

class UpperCaseExecutionStep(ExecutionStep):
    # in text str
    # out result str
    def execute(self):
        self.result = self.text.upper()

class UserInputExecutionStep(ExecutionStep):
    # in message str
    # out input str
    def execute(self):
        self.input = input(self.message)

execution_steps_definition = {
    "Print": PrintExecutionStep,
    "UpperCase": UpperCaseExecutionStep,
    "UserInput": UserInputExecutionStep
}
