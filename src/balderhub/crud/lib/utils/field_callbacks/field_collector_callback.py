from typing import Any
from abc import ABC, abstractmethod

import balder
from .base_field_callback import BaseItemMappingCallback, CallbackElementObjectT


class CollectItemmappingCallback(BaseItemMappingCallback, ABC):
    """
    Specific data item field callback for collecting the value of a specific field
    """

    @abstractmethod
    def execute(
            self,
            feature: balder.Feature,
            field: str,
            element_object: CallbackElementObjectT,
            already_collected_data: Any
    ) -> Any:
        """
        Executes the collecting of the specific field value.
        :param feature: the balder feature that calls this callback
        :param field: the field name
        :param element_object: the element object
        :param already_collected_data: all data that was already collected
        """
