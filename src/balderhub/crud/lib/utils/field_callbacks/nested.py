from __future__ import annotations
from typing import Any, Iterable

from balderhub.data.lib.utils import NOT_DEFINABLE, SingleDataItem, LookupFieldString
from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature


from .base_field_callback import BaseFieldCallback, CallbackElementObjectT
from .field_collector_callback import FieldCollectorCallback
from .field_filler_callback import FieldFillerCallback

class Nested(BaseFieldCallback):
    """
    Helper class to define nested field callbacks.
    """
    def __init__(self, __forward_none = True, **kwargs) -> None:
        super().__init__(**kwargs)
        self._nested_data = kwargs
        self.__forward_none = __forward_none
        self._inner_callback_type = None

        # now determine if the group is either only-collecting or only-filling
        for _, cur_callback in self._nested_data.items():
            if not isinstance(cur_callback, BaseFieldCallback):
                raise TypeError(f'the nested elements need to define a callback (base type: '
                                f'`{BaseFieldCallback.__name__}`)')
            if isinstance(cur_callback, (FieldCollectorCallback, FieldFillerCallback)):
                cur_callback_type = \
                    FieldCollectorCallback if isinstance(cur_callback, FieldCollectorCallback) else FieldFillerCallback
            elif isinstance(cur_callback, Nested):
                cur_callback_type = cur_callback.inner_callback_type
            else:
                raise TypeError(f'the nested elements need to define a valid callback '
                                f'(`{FieldCollectorCallback.__name__}`, `{FieldFillerCallback.__name__}` '
                                f'or `{Nested.__name__}`)')
            if self._inner_callback_type is None:
                self._inner_callback_type = cur_callback_type
            else:
                if self._inner_callback_type != cur_callback_type:
                    raise TypeError(f'it is not allowed to provide different kinds of inner callbacks, either provide '
                                    f'`{FieldCollectorCallback.__name__}` or `{FieldFillerCallback.__name__}` '
                                    f'(`{Nested.__name__}` need to have the same types for their nested elements)')
        if self._inner_callback_type is None:
            raise TypeError(f'it is not allowed to provide `{Nested.__name__}` only or empty `{Nested.__name__}` '
                            f'definitions')

    @property
    def inner_callback_type(self) -> type[BaseFieldCallback]:
        """
        :return: returns the inner callback type (either `FieldCollectorCallback` or `FieldFillerCallback` depending
                 on the inner fields)
        """
        return self._inner_callback_type

    @classmethod
    def __has_other_values_than_none(cls, values: Iterable) -> bool:
        return max(cur_val is not None for cur_val in values if cur_val != NOT_DEFINABLE)


    def _fill_missing_values_with_not_definables(
            self,
            result_data,
            all_expected_subfields
    ):

        for cur_field in all_expected_subfields:
            if cur_field in result_data.keys():
                # already available -> skip
                continue
            result_data[cur_field] = NOT_DEFINABLE
        return result_data

    def _execute_for_collecting(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: dict[str, Any],
            **kwargs
    ) -> dict[str, Any] | None:

        cur_data_item_type = feature.data_item_type.get_field_data_type(abs_field_name)
        if not issubclass(cur_data_item_type, SingleDataItem):
            raise TypeError(f'field with Nested callback `{cur_data_item_type}` is not a data item')

        all_expected_subfields = cur_data_item_type.get_all_fields_for(nested=False)

        if not isinstance(already_collected_data, dict):
            raise TypeError(f'the `already_collected_data` element needs to be from type `dict`, '
                            f'but it is from type `{type(already_collected_data)}`')

        result_data = {}
        # now execute data for every field and return related data item
        for cur_sub_field, cur_sub_callback in self._nested_data.items():
            # validate that the field is expected
            if cur_sub_field not in all_expected_subfields:
                raise KeyError(f'can not find mentioned field `{cur_sub_field}` in data item type '
                               f'`{cur_data_item_type.__name__}`')
            # the absolute lookup for the current sub field
            cur_absolute_sub_field = LookupFieldString(abs_field_name, cur_sub_field)

            result_data[cur_sub_field] = cur_sub_callback.execute(
                feature=feature,
                abs_field_name=cur_absolute_sub_field,
                element_object=element_object,
                already_collected_data=result_data,
                **kwargs
            )

        if self.__forward_none and not self.__has_other_values_than_none(result_data.values()):
            # if all values are `None` -> return None
            if not feature.data_item_type.is_optional_field(abs_field_name):
                raise ValueError(f'the field `{abs_field_name}` of `{feature.data_item_type}` can not be None '
                                 f'(non optional)')
            return None

        return self._fill_missing_values_with_not_definables(
            result_data=result_data,
            all_expected_subfields=all_expected_subfields
        )

    def _execute_for_filling(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            field_value_to_fill: dict[str, Any],
            already_filled_data: dict[str, Any],
            **kwargs
        ) -> dict[str, Any] | None:

        cur_data_item_type = feature.data_item_type.get_field_data_type(abs_field_name)
        if not issubclass(cur_data_item_type, SingleDataItem):
            raise TypeError(f'field with Nested callback `{cur_data_item_type}` is not a data item')

        if not isinstance(already_filled_data, dict):
            raise TypeError(f'the `already_collected_data` element needs to be from type `dict`, '
                            f'but it is from type `{type(already_filled_data)}`')

        if not isinstance(field_value_to_fill, dict):
            raise TypeError(f'the item data needs to be from type `dict`, but it is from type '
                            f'`{type(field_value_to_fill)}`')

        all_expected_subfields = cur_data_item_type.get_all_fields_for(nested=False)

        result_data = {}
        # now execute data for every field and return related data item
        for cur_sub_field, cur_sub_callback in self._nested_data.items():
            # validate that the field is expected
            if cur_sub_field not in all_expected_subfields:
                raise KeyError(f'can not find mentioned field `{cur_sub_field}` in data item type '
                               f'`{cur_data_item_type.__name__}`')
            # the absolute lookup for the current sub field
            if cur_sub_field not in field_value_to_fill:
                raise KeyError(f'can not find mentioned field `{cur_sub_field}` in provided data to fill '
                               f'dictionary: {field_value_to_fill}')

            cur_absolute_sub_field = abs_field_name.add_sub_field(cur_sub_field)
            cur_sub_field_val = field_value_to_fill[cur_sub_field]

            if cur_sub_field_val == NOT_DEFINABLE:
                result_data[cur_sub_field] = NOT_DEFINABLE
            else:
                result_data[cur_sub_field] = cur_sub_callback.execute(
                    feature=feature,
                    abs_field_name=cur_absolute_sub_field,
                    element_object=element_object,
                    field_value_to_fill=cur_sub_field_val,
                    already_filled_data=result_data,
                    **kwargs
                )

        all_fields_are_not_definable = min(cur_val == NOT_DEFINABLE for cur_val in result_data.values())
        if all_fields_are_not_definable:
            return NOT_DEFINABLE

        if self.__forward_none and not self.__has_other_values_than_none(result_data.values()):
            # if all values are `None` -> return None
            if not feature.data_item_type.is_optional_field(abs_field_name):
                raise ValueError(f'the field `{abs_field_name}` of `{feature.data_item_type}` can not be None '
                                 f'(non optional)')
            return None

        return self._fill_missing_values_with_not_definables(
            result_data=result_data,
            all_expected_subfields=all_expected_subfields
        )

    # pylint: disable=arguments-differ
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: str,
            element_object: CallbackElementObjectT,
            **kwargs
    ) -> Any:
        """
        Executes the nested statement with all its inner callbacks.

        :param feature: the balder feature that calls this callback
        :param abs_field_name: the field name
        :param element_object: the working element describing one single container the data can be collected or filled
                               in
        """
        abs_field_name = LookupFieldString(abs_field_name)

        if self.inner_callback_type == FieldCollectorCallback:
            return self._execute_for_collecting(feature, abs_field_name, element_object, **kwargs)
        if self.inner_callback_type == FieldFillerCallback:
            return self._execute_for_filling(feature, abs_field_name, element_object, **kwargs)
        raise TypeError(f'the inner callback type `{self.inner_callback_type}` is not supported')
