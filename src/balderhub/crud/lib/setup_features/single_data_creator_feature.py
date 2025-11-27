from typing import Dict, TypeVar

from balderhub.data.lib.utils import SingleDataItem, NOT_DEFINABLE

from balderhub.crud.lib.utils.exceptions import CallbackExecutionError
from balderhub.crud.lib import scenario_features
from balderhub.crud.lib.utils.item_mapping import FillItemmappingCallback

ElementContainerTypeT = TypeVar('ElementContainerTypeT')


class SingleDataCreatorFeature(scenario_features.SingleDataCreatorFeature):
    """
    Setup creating feature with field callback mapping
    """

    def item_mapping(self) -> Dict[str, FillItemmappingCallback]:
        """returns a dictionary with the dataclass field name as key and its configuration as value"""
        raise NotImplementedError

    def get_element_container(self) -> ElementContainerTypeT:
        """
        This method returns a custom object that will be given to any callback.
        :return:
        """
        raise NotImplementedError

    def fill(self, data_class: SingleDataItem):

        element_data = {}

        # TODO what about sub field is not None if current optional field is None
        element_container = self.get_element_container()
        cur_item_mapping = self.item_mapping()

        # iterate over all existing fields
        for cur_field_name in self.data_item_type.get_all_fields_for(nested=False):
            cur_field_val = data_class.get_field_value(cur_field_name)

            # the field needs to be in `self.item_mapping` or in `self.non_fillable_resolved_fields`
            if self.is_non_fillable_field(cur_field_name):
                element_data[cur_field_name] = NOT_DEFINABLE
            elif cur_field_val == NOT_DEFINABLE or \
                    isinstance(cur_field_val, SingleDataItem) and cur_field_val.all_fields_are_not_definable():
                # do not forward it
                element_data[cur_field_name] = NOT_DEFINABLE
            elif cur_field_name in cur_item_mapping.keys():

                cur_callback = cur_item_mapping[cur_field_name]
                try:
                    element_data[cur_field_name] = cur_callback.execute(
                        self,
                        cur_field_name,
                        element_container,
                        data_to_fill=data_class
                    )
                except Exception as exc:
                    raise CallbackExecutionError(
                        f'error while executing callback `{cur_callback}` for field `{cur_field_name}`'
                    ) from exc
            else:
                raise KeyError(f'not mentioned field `{cur_field_name}` in {self.__class__.__name__} for data item '
                               f'`{self.data_item_type}`')

        return self.data_item_type.create_as_nested(**element_data)
