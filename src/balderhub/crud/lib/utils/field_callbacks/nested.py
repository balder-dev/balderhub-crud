from __future__ import annotations
from typing import Any, Iterable

from balderhub.data.lib.utils import NOT_DEFINABLE, SingleDataItem
from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from . import FieldCollectorCallback, FieldFillerCallback
from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


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


    def _execute_for_collecting(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            already_collected_data: SingleDataItem,
            **kwargs
    ):

        cur_data_item_type, cur_data_item_optional = feature.data_item_type.get_field_data_type(field)
        all_expected_fields = cur_data_item_type.get_all_fields_for(nested=False)

        if not isinstance(already_collected_data, feature.data_item_type):
            raise TypeError(f'the `already_collected_data` element needs to be from type `{feature.data_item_type}`, '
                            f'but it is from type `{type(already_collected_data)}`')

        cur_data_item = already_collected_data.get_field_value(field)

        # TODO WORKAROUND - WE NEED A SOLUTION FOR THAT!!!
        if cur_data_item is None:
            # TODO normally we should provide None everywhere!! Only NOT_DEFINABLE will be ignored!
            return None

        if not isinstance(cur_data_item, cur_data_item_type):
            raise TypeError(f'the item data of nested field `{field}` needs to be from type `{cur_data_item_type}`, '
                            f'but it is from type `{type(cur_data_item)}`')

        result_data = {}
        # now execute data for every field and return related data item
        for cur_sub_field, cur_sub_callback in self._nested_data.items():
            # validate that the field is expected
            if cur_sub_field not in all_expected_fields:
                raise KeyError(f'can not find mentioned field `{cur_sub_field}` in data item type '
                               f'`{cur_data_item_type.__name__}`')
            # the absolute lookup for the current sub field
            cur_absolute_sub_field = f'{field}__{cur_sub_field}'

            result_data[cur_sub_field] = cur_sub_callback.execute(
                feature=feature,
                field=cur_absolute_sub_field,
                element_object=element_object,
                already_collected_data=already_collected_data,
                **kwargs
            )

        if self.__forward_none and not self.__has_other_values_than_none(result_data.values()):
            # if all values are `None` -> return None
            if not cur_data_item_optional:
                raise ValueError(f'the field `{field}` of `{feature.data_item_type}` can not be None '
                                 f'(non optional)')
            return None

        for cur_field in all_expected_fields:
            if cur_field in result_data.keys():
                # already available -> skip
                continue
            result_data[cur_field] = NOT_DEFINABLE
        return result_data

    def _execute_for_filling(
                self,
                feature: AbstractDataItemRelatedFeature,
                field: str,
                element_object: CallbackElementObjectT,
                data_to_fill: SingleDataItem,
                **kwargs
        ):

        cur_data_item_type, cur_data_item_optional = feature.data_item_type.get_field_data_type(field)
        all_expected_fields = cur_data_item_type.get_all_fields_for(nested=False)

        if not isinstance(data_to_fill, feature.data_item_type):
            raise TypeError(f'the item data needs to be from type `{feature.data_item_type}`, but it is from type '
                            f'`{type(data_to_fill)}`')
        cur_data_item = data_to_fill.get_field_value(field)

        # TODO WORKAROUND - WE NEED A SOLUTION FOR THAT!!!
        if cur_data_item is None:
            # TODO normally we should provide None everywhere!! Only NOT_DEFINABLE will be ignored!
            return None

        if not isinstance(cur_data_item, cur_data_item_type):
            raise TypeError(f'the item data of nested field `{field}` needs to be from type `{cur_data_item_type}`, '
                            f'but it is from type `{type(cur_data_item)}`')

        result_data = {}
        # now execute data for every field and return related data item
        for cur_sub_field, cur_sub_callback in self._nested_data.items():
            # validate that the field is expected
            if cur_sub_field not in all_expected_fields:
                raise KeyError(f'can not find mentioned field `{cur_sub_field}` in data item type '
                               f'`{cur_data_item_type.__name__}`')
            # the absolute lookup for the current sub field
            cur_absolute_sub_field = f'{field}__{cur_sub_field}'
            cur_sub_field_val = data_to_fill.get_field_value(cur_absolute_sub_field)

            if cur_sub_field_val == NOT_DEFINABLE:
                result_data[cur_sub_field] = NOT_DEFINABLE
            else:
                result_data[cur_sub_field] = cur_sub_callback.execute(
                    feature=feature,
                    field=cur_absolute_sub_field,
                    element_object=element_object,
                    data_to_fill=data_to_fill, # TODO??
                    **kwargs
                )

        all_fields_are_not_definable = min(cur_val == NOT_DEFINABLE for cur_val in result_data.values())
        if all_fields_are_not_definable:
            return NOT_DEFINABLE

        if self.__forward_none and not self.__has_other_values_than_none(result_data.values()):
            # if all values are `None` -> return None
            if not cur_data_item_optional:
                raise ValueError(f'the field `{field}` of `{feature.data_item_type}` can not be None '
                                 f'(non optional)')
            return None

        for cur_field in all_expected_fields:
            if cur_field in result_data.keys():
                # already available -> skip
                continue
            result_data[cur_field] = NOT_DEFINABLE
        return result_data

    # pylint: disable=arguments-differ
    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            **kwargs
    ) -> Any:
        """
        Executes the nested statement with all its inner callbacks.

        :param feature: the balder feature that calls this callback
        :param field: the field name
        :param element_object: the working element describing one single container the data can be collected or filled
                               in
        """
        if self.inner_callback_type == FieldCollectorCallback:
            return self._execute_for_collecting(feature, field, element_object, **kwargs)
        if self.inner_callback_type == FieldFillerCallback:
            return self._execute_for_filling(feature, field, element_object, **kwargs)
        raise TypeError(f'the inner callback type `{self.inner_callback_type}` is not supported')
