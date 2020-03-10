from etl.common import StepController


class ConsoleInput(StepController):
    def input_text(self, message: str):
        return input(message)
