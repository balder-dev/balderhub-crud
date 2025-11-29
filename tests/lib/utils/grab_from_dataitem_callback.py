from typing import Any

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from balderhub.data.lib.utils import SingleDataItem
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT


class GrabFromDataitemCallback(FieldCollectorCallback):

    def __init__(self):
        super().__init__()

    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            already_collected_data: SingleDataItem,
            **kwargs
    ) -> Any:
        return element_object.get_field_value(field)
