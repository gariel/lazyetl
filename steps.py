
execution_steps_definition = {}


def executionStep(key, input={}, output={}):
    def decorator(clzz):
        fields = input.copy()
        fields.update(output)
        execution_steps_definition[key] = clzz

        clzz.__step_input__ = input
        clzz.__step_output__ = output
        clzz.__step_key__ = key

        init = clzz.__init__
        def esInit(self, *args, **kwargs):
            for field, valuefunc in fields.items():
                setattr(self, field, valuefunc())
            init(self, *args, **kwargs)
        clzz.__init__ = esInit
        return clzz
    return decorator


@executionStep("Print",
    input={"text": str})
class PrintExecutionStep:
    def execute(self):
        print(self.text)


@executionStep("UpperCase",
    input={"text": str},
    output={"result": str})
class UpperCaseExecutionStep:
    def execute(self):
        self.result = self.text.upper()


@executionStep("UserInput",
    input={"text": str},
    output={"input": str})
class UserInputExecutionStep:
    def execute(self):
        self.input = input(self.message)
