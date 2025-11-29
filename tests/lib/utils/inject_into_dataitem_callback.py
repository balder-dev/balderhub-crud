from typing import Any

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from balderhub.data.lib.utils import SingleDataItem
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT


# TODO improve that - maybe provide different ones


class InjectIntoDataitemCallback(FieldFillerCallback):

    def __init__(self):
        super().__init__()

    def execute(
            self,
            feature: AbstractDataItemRelatedFeature,
            field: str,
            element_object: CallbackElementObjectT,
            data_to_fill: SingleDataItem,
            **kwargs
    ) -> Any:
        element_object.set_field_value(field, data_to_fill.get_field_value(field))
        return data_to_fill
