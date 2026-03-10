from __future__ import annotations
from typing import List, Dict, Union, Any


import balder
import balderhub.data

from balderhub.data.lib.setup_features import factories
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage, NOT_DEFINABLE

from balderhub.crud.lib.setup_features import SingleUpdaterFeature
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.utils.inject_into_dict_callback import InjectIntoDictCallback


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class SingleCategoryUpdator(SingleUpdaterFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._id_to_update = None
        self._data: Union[dict[str, Any], None] = None
        self._last_exception = None

    def load(self, unique_identification_value: Any):
        self._data = {}
        self._id_to_update = unique_identification_value

    def get_non_fillable_fields(self) -> List[str]:
        return ['id']

    def get_element_container(self) -> dict[str, Any]:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'name': InjectIntoDictCallback()
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        try:
            self.Dut.sim.dut_simulator.update_in_category(with_id=self._id_to_update, data_to_update=self._data)
            self._data = None
            self._id_to_update = None
        except Exception as e:
            self._last_exception = e

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
