import enum
import re
from .loader import load_module


class OperationType(enum.Enum):
    FILTER = enum.auto()
    TRANSFORM = enum.auto()


class FunctionFilter:
    def __init__(self, function: str):
        self._func = load_module(function)

    def get_operation_type(self) -> OperationType:
        return OperationType.FILTER

    def __call__(self, conv) -> bool:
        return self._func(conv)


class MaxLenFilter:
    def __init__(self, max_len: int):
        self._max_len = max_len

    def get_operation_type(self) -> OperationType:
        return OperationType.FILTER

    def __call__(self, conv) -> bool:
        return all(len(text) <= self._max_len for text in conv)


class MinLenFilter:
    def __init__(self, min_len):
        self._min_len = min_len

    def get_operation_type(self):
        return OperationType.FILTER

    def __call__(self, conv):
        return all(len(text) >= self._min_len for text in conv)


class MaxTurnFilter:
    def __init__(self, max_turn):
        self._max_turn = max_turn

    def get_operation_type(self):
        return OperationType.FILTER

    def __call__(self, conv):
        return len(conv) <= self._max_turn


class MinTurnFilter:
    def __init__(self, min_turn):
        self._min_turn = min_turn

    def get_operation_type(self):
        return OperationType.FILTER

    def __call__(self, conv):
        return len(conv) >= self._min_turn


class DenyRegexFilter:
    def __init__(self, regex):
        self._regex = regex

    def get_operation_type(self):
        return OperationType.FILTER

    def __call__(self, conv):
        return not any(re.search(self._regex, text) for text in conv)


class FunctionTransform:
    def __init__(self, function: str):
        self._func = load_module(function)

    def get_operation_type(self) -> OperationType:
        return OperationType.TRANSFORM

    def __call__(self, conv) -> bool:
        return self._func(conv)


class ReplaceTransform:
    def __init__(self, regex: str, replacement: str):
        self._regex = regex
        self._replacement = replacement

    def get_operation_type(self):
        return OperationType.TRANSFORM

    def __call__(self, conv):
        return [re.sub(pattern=self._regex, repl=self._replacement, string=s) for s in conv]
