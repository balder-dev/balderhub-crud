from __future__ import annotations
from typing import Any

from balderhub.data.lib.utils import NOT_DEFINABLE
from balderhub.data.lib.utils.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from .base_field_callback import BaseFieldCallback, CallbackElementObjectT


class Nested(BaseFieldCallback):
    """
    Helper class to define nested field callbacks.
    """
    def __init__(self, __forward_none = True, **kwargs) -> None:
        super().__init__(**kwargs)
        self._nested_data = kwargs
        self.__forward_none = __forward_none
        # TODO validate that data is correct?

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
        :param element_object: the working element describing one single container the data can be collected or filled in
        """
        # TODO WORKAROUND - WE NEED A BETTER SOLUTION FOR THAT
        from balderhub.crud.lib.setup_features import SingleDataReaderFeature, MultipleDataReaderFeature
        item_data = kwargs['already_collected_data'] if 'already_collected_data' in kwargs else kwargs['data_to_fill']
        is_collecting = isinstance(feature, (SingleDataReaderFeature, MultipleDataReaderFeature))

        if not hasattr(feature, 'data_item_type'):
            raise TypeError(f'this mapping class can not work with features from type `{feature.__class__}`')
        feature_data_item_type = getattr(feature, 'data_item_type')
        cur_data_item_type, cur_data_item_optional = feature_data_item_type.get_field_data_type(field)
        all_expected_fields = cur_data_item_type.get_all_fields_for(nested=False)

        if not isinstance(item_data, feature_data_item_type):
            raise TypeError(f'the item data needs to be from type `{feature_data_item_type}`, but it is from type '
                            f'`{type(item_data)}`')
        cur_data_item = item_data.get_field_value(field)

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
            cur_sub_field_val = item_data.get_field_value(cur_absolute_sub_field)

            # TODO problematic - different behavior for fill()/collect()
            if not is_collecting and cur_sub_field_val == NOT_DEFINABLE:
                result_data[cur_sub_field] = NOT_DEFINABLE
            else:
                cb_result = cur_sub_callback.execute(feature, cur_absolute_sub_field, element_object, **kwargs)
                result_data[cur_sub_field] = cb_result

        all_fields_are_not_definable = min([cur_val == NOT_DEFINABLE for cur_val in result_data.values()])
        if all_fields_are_not_definable:
            return NOT_DEFINABLE

        if self.__forward_none:
            # if all values are `None` -> return None
            has_other_val_than_none = max(
                [cur_val is not None for cur_val in result_data.values() if cur_val != NOT_DEFINABLE]
            )
            if not has_other_val_than_none:
                if not cur_data_item_optional:
                    raise ValueError(f'the field `{field}` of `{feature_data_item_type}` can not be None '
                                     f'(non optional)')
                return None

        for cur_field in all_expected_fields:
            if cur_field in result_data.keys():
                # already available -> skip
                continue
            result_data[cur_field] = NOT_DEFINABLE
        return result_data
