from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TypeVar


CallbackElementObjectT = TypeVar('CallbackElementObjectT')


class BaseFieldCallback(ABC):
    """
    Base class for data item field callbacks.

    These callbacks will be called for every field while interacting with the system-under-test.
    """
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """
        This method executes the callback.
        """
