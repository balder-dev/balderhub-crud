from typing import Any

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature

from balderhub.data.lib.utils import SingleDataItem, LookupFieldString

from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import CallbackElementObjectT


# TODO improve that - maybe provide different ones


class InjectIntoDictCallback(FieldFillerCallback):

    def __init__(self):
        super().__init__()

    def _fill_in(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            field_value_to_fill: Any,
            already_filled_data: dict[str, Any],
            **kwargs
    ):

        element_object[str(abs_field_name)] = field_value_to_fill
        return field_value_to_fill
    
    def _unset_field(
            self,
            feature: AbstractDataItemRelatedFeature,
            abs_field_name: LookupFieldString,
            element_object: CallbackElementObjectT,
            already_filled_data: dict[str, Any],
            **kwargs
    ) -> Any:
        element_object[str(abs_field_name)] = UNSET
        return UNSET
