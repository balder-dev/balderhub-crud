from typing import Any

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from balderhub.data.lib.utils import SingleDataItem, LookupFieldString
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT


class GrabFromDictCallback(FieldCollectorCallback):

    def __init__(self):
        super().__init__()

    def _collect_field_value(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_collected_data: SingleDataItem,
            **kwargs
    ) -> Any:
        if str(abs_field_name) not in element_object:
            while True:
                upper_path_field_keys = abs_field_name.split_field_keys[:-1]
                if len(upper_path_field_keys) == 0:
                    raise ValueError('can not find a key')
                abs_field_name = LookupFieldString(*upper_path_field_keys)
                if str(abs_field_name) in element_object:
                    return element_object[str(abs_field_name)]
        return element_object[str(abs_field_name)]
