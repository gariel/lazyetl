from unittest import TestCase

import steps
from jobrunner import JobRunner
from structure import (
    Parameter,
    Field,
    Step,
    Sequence,
    Link,
    Job
)


class JobRunnerTest(TestCase):

    def set_step(self, func):
        class TestStep:
            def __init__(self):
                self.input = ""
                self.output = ""

            def execute(self):
                self.output = func(self.input)
        steps.execution_steps_definition["Test"] = TestStep

    def create_step(self, id, input, outputvar):
        step = Step()
        step.type = "Test"
        step.id = id

        param = Parameter()
        param.name = "input"
        param.type = "str"
        param.value = input
        step.parameters.append(param)

        field = Field()
        field.name = "output"
        field.type = "str"
        field.variable = outputvar
        step.fields.append(field)

        return step

    def setUp(self):
        self.jr = JobRunner()

    def test_should_execute_step(self):
        def step(input):
            self.assertEqual(input, "asd")
        self.set_step(step)

        job = Job()
        job.steps.append(self.create_step("1", "asd", "out"))

        seq = Sequence()
        seq.first = "1"
        job.sequence = seq

        self.jr.run(job)

    def test_should_set_output(self):
        def step(input):
            if input[0] == "1":
                return "AAA"
            else:
                self.assertEqual(input, "2AAA")
        self.set_step(step)

        job = Job()
        job.steps.append(self.create_step("1", "1asd", "out"))
        job.steps.append(self.create_step("2", "2{{out}}", "out2"))


        seq = Sequence()
        seq.first = "1"
        job.sequence = seq

        self.jr.run(job)        



