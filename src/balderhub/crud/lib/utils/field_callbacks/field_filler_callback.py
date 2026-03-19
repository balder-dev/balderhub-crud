from typing import Any
from abc import ABC, abstractmethod

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils import LookupFieldString

from .base_field_callback import BaseFieldCallback, CallbackElementObjectT
from ..unset import UNSET


class FieldFillerCallback(BaseFieldCallback, ABC):
    """
    Specific data item field callback for filling a specific value into a specific field
    """

    # pylint: disable=arguments-differ
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString | str,
            element_object: CallbackElementObjectT,
            field_value_to_fill: Any,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        """
        Executes the filling of the specific field value.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be filled in
        :param field_value_to_fill: the field data that should be filled in
        :param already_filled_data: a dictionary with all field names and values that has already been filled
        :return: the filled field value
        """
        abs_field_name = LookupFieldString(abs_field_name)

        if field_value_to_fill is UNSET or \
                feature.data_item_type.is_optional_field(abs_field_name) and field_value_to_fill is None:
            return self._unset_field(
                feature=feature,
                abs_field_name=abs_field_name,
                element_object=element_object,
                already_filled_data=already_filled_data,
                **kwargs
            )

        return self._fill_in(
            feature=feature,
            abs_field_name=abs_field_name,
            element_object=element_object,
            field_value_to_fill=field_value_to_fill,
            already_filled_data=already_filled_data,
            **kwargs
        )

    @abstractmethod
    def _fill_in(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            field_value_to_fill: Any,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        """
        Callback that needs to be overwritten by child class. It should execute the filling process.

        .. note::
            The method :meth:`FieldFillerCallback.unset_field` will be called if the value should be UNSET.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be filled in
        :param field_value_to_fill: the field data that should be filled in
        :param already_filled_data: a dictionary with all field names and values that has already been filled
        :return: the filled field value
        """

    @abstractmethod
    def _unset_field(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        """
        Callback that needs to be overwritten by child class. It should unset the provided field.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be filled in
        :param already_filled_data: a dictionary with all field names and values that has already been filled
        :return: the filled field value
        """
