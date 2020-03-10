import abc
import io
import os
from typing import List, Optional

from etl.common import StatefulStepController


class File(StatefulStepController, abc.ABC):
    filename: str = ""

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode
        self.file: Optional[io.TextIOWrapper] = None

    def __start__(self):
        self.file = io.open(self.filename, self.mode)

    def __finish__(self):
        self.file.flush()
        self.file.close()


class FileRead(File):
    def __init__(self):
        super().__init__("r")

    def read(self) -> str:
        return self.file.read()

    def read_lines(self) -> List[str]:
        return self.file.readlines()


class FileWrite(File):
    def __init__(self):
        super().__init__("w")

    def write(self, data: str) -> None:
        self.file.write(data)

    def write_lines(self, data: List[str]) -> None:
        self.write(os.linesep.join([d.rstrip(os.linesep) for d in data]))

    def new_line(self) -> None:
        self.file.write(os.linesep)


class FileAppend(FileWrite):
    def __init__(self):
        File.__init__(self, "a")
