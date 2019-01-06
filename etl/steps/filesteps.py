
import io
from steps import executionStep


@executionStep(
    input={"filename", str},
    output={"content", str})
class ReadFileStep:
    mode = "r"
    def execute(self):
        with io.open(self.filename, type(self).mode) as f:
            self.content = f.read()

@executionStep(
    input={"filename", str},
    output={"content", bytes})
class ReadBinaryFileStep(ReadFileStep):
    mode = "rb"


@executionStep(
    input={"filename", str, 
            "content", str,
            "append", bool})
class WriteFileStep:
    modefunc = lambda append: "a" if append else "w"
    def execute(self):
        with io.open(self.filename, type(self).modefunc()) as f:
            f.write(self.content)

@executionStep(
    input={"filename", str, 
            "content", bytes,
            "append", bool})
class WriteBinaryFileStep(WriteFileStep):
    modefunc = lambda append: "ab" if append else "wb"
