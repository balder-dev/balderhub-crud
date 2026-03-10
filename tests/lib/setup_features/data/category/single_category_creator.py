from __future__ import annotations
from typing import Union, Any

import balder
import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage

from balderhub.crud.lib.setup_features import SingleCreatorFeature
from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.utils.inject_into_dict_callback import InjectIntoDictCallback


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class SingleCategoryCreator(SingleCreatorFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: Union[dict[str, Any], None] = None
        self._last_exception = None

    def load(self):
        self._data = {}

    def get_non_fillable_fields(self) -> list[str]:
        return ['id']

    def get_element_container(self) -> dict[str, Any]:
        return self._data

    def item_mapping(self) -> dict[str, FieldFillerCallback]:
        return {
            'name': InjectIntoDictCallback()
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        try:
            self.Dut.sim.dut_simulator.add_category(**{k: v for k, v in self._data.items() if v != UNSET})
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data: dict[str, Any],
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(f"DutSimulator.add_category() missing 1 required positional argument: '{without_mandatory_field}'")])

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
