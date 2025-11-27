from typing import List, Dict, TypeVar

from balderhub.data.lib.utils import SingleDataItemCollection


from balderhub.crud.lib import scenario_features
from balderhub.crud.lib.utils.exceptions import CallbackExecutionError
from balderhub.crud.lib.utils.item_mapping import CollectItemmappingCallback


ElementListItemContainerTypeT = TypeVar('ElementListItemContainerTypeT')


class MultipleDataReaderFeature(scenario_features.MultipleDataReaderFeature):
    """
    Setup multiple-reader feature with field callback mapping
    """

    def load(self):
        raise NotImplementedError

    def get_list_item_element_container(self) -> List[ElementListItemContainerTypeT]:
        """this callback collects the data of the table and returns a dictionary with the unique id as key and the data
        as value"""
        raise NotImplementedError

    def item_mapping(self) -> Dict[str, CollectItemmappingCallback]:
        """returns a dictionary with the dataclass field name as key and the callback that returns the data for this
        field as value - the value is a tuple with the callback on the first place and the parameter afterwards"""
        raise NotImplementedError

    def collect(self) -> SingleDataItemCollection:
        all_elements = []

        for cur_list_item_element_container in self.get_list_item_element_container():
            cur_item_mapping = self.item_mapping()

            new_dataclass = self.data_item_type.create_non_definable()
            all_elements.append(new_dataclass)

            # iterate over all existing fields
            for cur_field_name in self.data_item_type.get_all_fields_for(nested=False):
                # the field needs to be in `self.item_mapping` or in `self.resolved_non_collectable_fields`
                if self.is_non_collectable_field(cur_field_name):
                    # ignore - is already NOT_DEFINABLE
                    continue
                elif cur_field_name in cur_item_mapping.keys():
                    cur_callback = cur_item_mapping[cur_field_name]
                    try:
                        element_data = cur_callback.execute(
                            self,
                            cur_field_name,
                            cur_list_item_element_container,
                            already_collected_data=new_dataclass
                        )
                        new_dataclass.set_field_value(cur_field_name, element_data)
                    except Exception as exc:
                        raise CallbackExecutionError(
                            f'error while executing callback `{cur_callback}` for field `{cur_field_name}`'
                        ) from exc
                else:
                    raise KeyError(f'not mentioned field `{cur_field_name}` in {self.__class__.__name__} for data item '
                                   f'`{cur_list_item_element_container}`')



        return SingleDataItemCollection(all_elements)
