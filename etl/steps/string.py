import re
from typing import List

from etl.common import StepController


class String(StepController):
    def lower_case(self, text: str) -> str:
        return text.lower()

    def upper_case(self, text: str) -> str:
        return text.upper()

    def split(self, text: str, char: str) -> List[str]:
        return text.split(char)

    def split_lines(self, text: str, keep_line_end: bool) -> List[str]:
        return text.splitlines(keep_line_end)

    def replace(self, text: str, old: str, new: str) -> str:
        return text.replace(old, new)

    def replace_regex(self, text: str, pattern: str, replacement: str, flags: re.RegexFlag = 0) -> str:
        regex = self.cache.regex_compile(pattern, flags)
        return regex.sub(replacement, text)
