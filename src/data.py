#
# data.py
#
# Authors: Artur Barichello
#          Lucas Verdade
#          Lucas Zacchi

# Data structures used in the semantic analysis step

import uuid
from collections import deque
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Tuple, Any, Deque
from output import VariableInScopeError
from enum import Enum, auto


class DataType(Enum):
    FUNC = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    NULL = auto()


@dataclass
class TreeNode:
    def __init__(
        self,
        left: Optional["TreeNode"],
        right: Optional["TreeNode"],
        value: Optional[Union[str, int, float]],
        res_type: str,
    ) -> None:
        self.id = uuid.uuid4()

        self.value = value
        self.left = left
        self.right = right
        self.res_type = res_type

    def as_dict(self) -> Dict:
        left = None if self.left is None else self.left.as_dict()
        right = None if self.right is None else self.right.as_dict()

        return {
            "value": self.value,
            "right": right,
            "left": left,
        }

    def __str_(self) -> str:
        return f"TreeNode id= {self.id} with value {self.value};"


@dataclass
class EntryTable:
    label: str
    datatype: str
    values: List[int]
    lineno: int

    def as_dict(self) -> Dict:
        return {
            "label": self.label,
            "datatype": self.datatype,
            "values": self.values,
            "lineno": self.lineno,
        }


class Scope:
    def __init__(self, outer_scope=None, loop=False) -> None:
        self.entry_table: List[EntryTable] = []
        self.outer_scope: Optional[Scope] = outer_scope
        self.inner_scopes: List = []
        self.loop: bool = loop

    def __str__(self) -> str:
        return str(entry for entry in self.entry_table)

    def add_entry(self, entry: EntryTable) -> None:
        has_var, lineno = self.contains_var(entry.label)

        if has_var:
            raise VariableInScopeError(
                f"Variável {entry.label} na linha {entry.lineno} já foi declarada na linha {lineno}"
            )
        self.entry_table.append(entry)

    def add_inner_scope(self, scope: Any) -> None:
        self.inner_scopes.append(scope)

    def contains_var(self, var_label: str) -> Tuple[bool, Union[int, None]]:
        for entry in self.entry_table:
            if entry.label == var_label:
                return True, entry.lineno
        return False, None

    def as_dict(self) -> Dict:
        return {
            "table": [entry.as_dict() for entry in self.entry_table],
            "inner_scopes": [scope.as_dict() for scope in self.inner_scopes],
        }


class ScopeStack:
    def __init__(self) -> None:
        self.stack: Deque[Scope] = deque()

    def __len__(self) -> int:
        return len(self.stack)

    def is_empty(self) -> bool:
        return True if len(self.stack) == 0 else False

    def length(self) -> int:
        return len(self.stack)

    def push(self, x: Scope) -> None:
        self.stack.append(x)

    def pop(self) -> Scope:
        return self.stack.pop()

    def seek(self) -> Optional[Scope]:
        if self.is_empty():
            return None
        else:
            return self.stack[-1]
