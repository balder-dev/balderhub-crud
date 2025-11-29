from typing import Any
from abc import ABC, abstractmethod

from balderhub.data.lib.utils import SingleDataItem
from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


class FieldFillerCallback(BaseFieldCallback, ABC):
    """
    Specific data item field callback for filling a specific value into a specific field
    """

    # pylint: disable=arguments-differ
    @abstractmethod
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            data_to_fill: SingleDataItem,
            **kwargs
    ) -> Any:
        """
        Executes the filling of the specific field value.

        :param feature: the balder feature that calls this callback
        :param field: the field name
        :param element_object: the working element describing one single container the data can be filled in
        :param data_to_fill: the data that should be filled in
        :return: the filled field value
        """
