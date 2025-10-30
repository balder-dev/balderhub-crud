from __future__ import annotations
from typing import Any, TypeVar

CallbackElementObjectT = TypeVar('CallbackElementObjectT')


class BaseItemMappingCallback:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError
