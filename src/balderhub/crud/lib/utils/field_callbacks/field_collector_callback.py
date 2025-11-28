from typing import Any
from abc import ABC, abstractmethod

from balderhub.data.lib.utils import SingleDataItem
from balderhub.data.lib.utils.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


class FieldCollectorCallback(BaseFieldCallback, ABC):
    """
    Specific data item field callback for collecting the value of a specific field
    """

    # pylint: disable=arguments-differ
    @abstractmethod
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            already_collected_data: SingleDataItem,
            **kwargs
    ) -> Any:
        """
        Executes the collecting of the specific field value.
        :param feature: the balder feature that calls this callback
        :param field: the field name
        :param element_object: the working element describing one single container the data can be collected
        :param already_collected_data: all data that was already collected
        :return: the collected field value
        """
