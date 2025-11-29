from __future__ import annotations
from typing import List, Dict, Union

import balder
import balderhub.data
from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList, ResponseMessage, NOT_DEFINABLE

from balderhub.crud.lib.setup_features import SingleDataCreatorFeature
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.utils.inject_into_dataitem_callback import InjectIntoDataitemCallback


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class SingleCategoryCreator(SingleDataCreatorFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: Union[BookCategoryDataItem, None] = None
        self._last_exception = None

    def load(self):
        self._data = BookCategoryDataItem(NOT_DEFINABLE, NOT_DEFINABLE)

    def get_non_fillable_fields(self) -> List[str]:
        return ['id']

    def get_element_container(self) -> BookCategoryDataItem:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'name': InjectIntoDataitemCallback()
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        parameter = {}
        if self._data.name != NOT_DEFINABLE:
            parameter['name'] = self._data.name

        try:
            self.Dut.sim.dut_simulator.add_category(**parameter)
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data_item: SingleDataItem,
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(f"DutSimulator.add_category() missing 1 required positional argument: '{without_mandatory_field}'")])

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
