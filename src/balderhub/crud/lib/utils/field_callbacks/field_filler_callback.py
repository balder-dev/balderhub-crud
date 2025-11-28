from typing import Any
from abc import ABC, abstractmethod

import balder
from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


class FillItemmappingCallback(BaseFieldCallback, ABC):
    """
    Specific data item field callback for filling a specific value into a specific field
    """

    @abstractmethod
    def execute(
            self,
            feature: balder.Feature,
            field: str,
            element_object: CallbackElementObjectT,
            data_to_fill: Any
    ) -> Any:
        """
        Executes the filling of the specific field value.

        :param feature: the balder feature that calls this callback
        :param field: the field name
        :param element_object: the element object
        :param data_to_fill: the data that should be filled in
        """
