from typing import Dict, TypeVar

from balderhub.data.lib.utils import SingleDataItem

from balderhub.crud.lib import scenario_features
from balderhub.crud.lib.utils.exceptions import CallbackExecutionError
from balderhub.crud.lib.utils.field_callbacks import CollectItemmappingCallback

ElementContainerTypeT = TypeVar('ElementContainerTypeT')


class SingleDataReaderFeature(scenario_features.SingleDataReaderFeature):
    """
    Setup single-read feature with field callback mapping
    """

    def item_mapping(self) -> Dict[str, CollectItemmappingCallback]:
        """returns a dictionary with the dataclass field name as key and the callback that returns the data for this
        field as value - the value is a tuple with the callback on the first place and the parameter afterwards"""
        raise NotImplementedError

    def get_element_container(self) -> ElementContainerTypeT:
        """
        This method returns a custom object that will be given to any callback.
        :return:
        """
        raise NotImplementedError

    def collect(self) -> SingleDataItem:
        new_dataclass = self.data_item_type.create_non_definable(nested=True)

        element_container = self.get_element_container()
        cur_item_mapping = self.item_mapping()

        # iterate over all existing fields
        for cur_field_name in self.data_item_type.get_all_fields_for(nested=False):
            # the field needs to be in `self.item_mapping` or in `self.non_collectable_resolved_fields`
            if self.is_non_collectable_field(cur_field_name):
                # ignore - is already NOT_DEFINABLE
                continue
            if cur_field_name not in cur_item_mapping.keys():
                raise KeyError(f'not mentioned field `{cur_field_name}` in {self.__class__.__name__} for data item '
                               f'`{self.data_item_type}`')
            cur_callback = cur_item_mapping[cur_field_name]
            try:
                element_data = cur_callback.execute(
                    self,
                    cur_field_name,
                    element_container,
                    already_collected_data=new_dataclass)
                new_dataclass.set_field_value(cur_field_name, element_data)
            except Exception as exc:
                raise CallbackExecutionError(
                    f'error while executing callback `{cur_callback}` for field `{cur_field_name}`'
                ) from exc

        return new_dataclass
