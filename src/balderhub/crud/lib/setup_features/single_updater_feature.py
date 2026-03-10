from typing import TypeVar, Any

from balderhub.data.lib.utils import NOT_DEFINABLE
from balderhub.data.lib.utils.functions import full_dictionary_is_not_definable

from balderhub.crud.lib import scenario_features
from balderhub.crud.lib.utils.exceptions import CallbackExecutionError
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

ElementContainerTypeT = TypeVar('ElementContainerTypeT')


class SingleUpdaterFeature(scenario_features.SingleUpdaterFeature):
    """
    Setup update feature with field callback mapping
    """

    def item_mapping(self) -> dict[str, FieldFillerCallback]:
        """returns a dictionary with the dataclass field name as key and its configuration as value"""
        raise NotImplementedError

    def get_element_container(self) -> ElementContainerTypeT:
        """
        This method returns a custom object that will be given to any callback.
        :return:
        """
        raise NotImplementedError

    def fill(self, data_class_dict: dict[str, Any]) -> dict[str, Any]:

        element_data = {}

        # TODO what about sub field is not None if current optional field is None
        element_container = self.get_element_container()
        cur_item_mapping = self.item_mapping()

        # iterate over all existing fields
        for cur_field_name in self.data_item_type.get_all_fields_for(nested=False):
            cur_field_val = data_class_dict[cur_field_name]

            # the field needs to be in `self.item_mapping` or in `self.non_fillable_resolved_fields`
            if self.is_non_fillable_field(cur_field_name):
                element_data[cur_field_name] = NOT_DEFINABLE
            elif cur_field_val == NOT_DEFINABLE:
                # do not call it for values that are NOT_DEFINABLE
                element_data[cur_field_name] = NOT_DEFINABLE
            elif isinstance(cur_field_val, dict) and full_dictionary_is_not_definable(cur_field_val):
                # do not forward it
                element_data[cur_field_name] = NOT_DEFINABLE
            elif cur_field_name in cur_item_mapping.keys():

                cur_callback = cur_item_mapping[cur_field_name]
                try:
                    element_data[cur_field_name] = cur_callback.execute(
                        self,
                        cur_field_name,
                        element_container,
                        field_value_to_fill=cur_field_val,
                        already_filled_data=element_data
                    )
                except Exception as exc:
                    raise CallbackExecutionError(
                        f'error while executing callback `{cur_callback}` for field `{cur_field_name}`'
                    ) from exc
            else:
                raise KeyError(f'not mentioned field `{cur_field_name}` in {self.__class__.__name__} for data item '
                               f'`{self.data_item_type}`')

        return element_data
