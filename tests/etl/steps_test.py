from unittest import TestCase

from steps import (
    executionStep,
    execution_steps_definition
)

class StepsTest(TestCase):
    def test_should_add_class_when_decorated_with_executionStep(self):
        @executionStep("Test")
        class Step:
            def execute(self):
                pass
        self.assertIn("Test", execution_steps_definition)
        self.assertIs(execution_steps_definition["Test"], Step)

    def test_should_create_variables_when_instatiate_a_decorated_step(self):
        @executionStep(
            input={"inputfield": str},
            output={"outputfield": int})
        class AStep:
            def execute(self):
                pass

        step = AStep()
        self.assertEqual(step.inputfield, "")
        self.assertEqual(step.outputfield, 0)

    def test_should_raise_exception_when_step_class_does_not_have_execute_method(self):
        def define_bad_step():
            @executionStep()
            class BadStep: 
                pass
        self.assertRaises(Exception, define_bad_step)
