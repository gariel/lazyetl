import abc
from typing import Any, Dict

from etl.common import Cache
from etl.steps.input import ConsoleInput
from etl.steps.logging import Logging, LogLevel
from etl.steps.string import String

import asyncio
import uvloop


class Runner:
    async def run(self, job: 'Job'):
        cache = Cache()

        async def do(step_name, data):
            # get step
            step = job.steps.get(step_name)

            # get method
            instance = job.instances[step.instance]
            instance.cache = cache
            method = getattr(instance, step.method)

            # call
            values = [a.get_value(data) for a in step.args]
            result = method(*values)

            # update data
            if not step.returns or type(step.returns) != tuple:
                result = (result,)

            if type(result[0]) == list:
                to_add = [(lv, *r[1:]) for r in result for lv in r[0]]
            else:
                to_add = [result]

            for add in to_add:
                next_data = data.copy()
                next_data.update({step.returns[i]: add[i] for i in range(len(step.returns))})

                # follow next
                to_all = step.follows.get('all')
                if to_all:
                    await do(to_all, next_data)

        await do(job.first, {})

# steps follows:
# everyone
# - all
# list
# - each
# bool
# - yes
# - no
# IO, search, xpath, single return
# - success
# - failed


async def start():
    job = Job()
    runner = Runner()
    await runner.run(job)


def main():
    uvloop.install()
    asyncio.run(start())


class Value(abc.ABC):
    @abc.abstractmethod
    def get_value(self, data: Dict[str, Any]) -> Any:
        pass


class Static(Value):
    def __init__(self, value: Any):
        self._value = value

    def get_value(self, _: Dict[str, Any]) -> Any:
        return self._value


class FormattedValue(Value):
    def __init__(self, value: str):
        self._value = value

    def get_value(self, data: Dict[str, Any]) -> Any:
        return self._value.format_map(data)


class Field(Value):
    def __init__(self, name: str):
        self._name = name

    def get_value(self, data: Dict[str, Any]) -> Any:
        return data.get(self._name)


class Step:
    def __init__(self, instance: str, method: str, *args: Value, follows={}, returns=tuple()):
        self.instance = instance
        self.method = method
        self.args = args
        self.follows = follows
        self.returns = returns


class Job:
    def __init__(self):
        self.instances = dict(
            string=String(),
            console_input=ConsoleInput(),
            logging=Logging()
        )
        self.first = "hello"
        self.steps = dict(
            hello=Step("logging", "log", Static(LogLevel.Info), Static("Hello World"), follows=dict(all='user_input')),
            user_input=Step("console_input", "input_text", Static("Type your name:"), follows=dict(all='log_username'), returns=("username",)),
            log_username=Step("logging", "log", Static(LogLevel.Info), FormattedValue("Inserted: {username}"), follows=dict(all='split_username')),
            split_username=Step("string", "split", Field("username"), Static(" "), follows=dict(all="username_upper"), returns=("username_part")),
            username_upper=Step("string", "upper_case", Field("username_part"), follows=dict(all='log_upper'), returns=("upper_username",)),
            log_upper=Step("logging", "log", Static(LogLevel.Info), FormattedValue("Username UPPER: {upper_username}")),
        )


if __name__ == '__main__':
    main()
