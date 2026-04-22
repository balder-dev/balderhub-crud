from typing import Any, Callable
from abc import ABC, abstractmethod

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString

from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


class FieldCollectorCallback(BaseFieldCallback, ABC):
    """
    Specific data item field callback for collecting the value of a specific field
    """

    def __init__(self, *args, type_convert_cb: Callable[[Any], Any] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._type_convert_cb = type_convert_cb

    # pylint: disable=arguments-differ
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString | str,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        """
        Executes the collecting of the specific field value.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be collected
        :param already_collected_data: all data that was already collected
        :return: the collected field value
        """
        abs_field_name = LookupFieldString(abs_field_name)
        result = self._collect_field_value(
            feature=feature,
            abs_field_name=abs_field_name,
            element_object=element_object,
            already_collected_data=already_collected_data
        )
        if self._type_convert_cb:
            return self._type_convert_cb(result)
        return result

    @abstractmethod
    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> Any:
        """
        Callback that needs to be overwritten by child class. It should execute the collecting process.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be collected
        :param already_collected_data: all data that was already collected
        :return: the collected field value
        """
