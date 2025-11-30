from __future__ import annotations
from typing import List, Dict, Union

import balder

import balderhub.data

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList, ResponseMessage, NOT_DEFINABLE

from balderhub.crud.lib.setup_features import SingleDataCreatorFeature
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import AuthorDataItem
from tests.lib.utils.inject_into_dataitem_callback import InjectIntoDataitemCallback


@balderhub.data.register_for_data_item(AuthorDataItem)
class SingleAuthorCreator(SingleDataCreatorFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data: Union[AuthorDataItem, None] = None

    def load(self):
        self._data = AuthorDataItem(id=NOT_DEFINABLE, first_name=NOT_DEFINABLE, last_name=NOT_DEFINABLE)

    def get_non_fillable_fields(self) -> List[str]:
        return ['id']

    def get_element_container(self) -> AuthorDataItem:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'first_name': InjectIntoDataitemCallback(),
            'last_name': InjectIntoDataitemCallback(),
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        parameter = {}
        if self._data.first_name != NOT_DEFINABLE:
            parameter['first_name'] = self._data.first_name
        if self._data.last_name != NOT_DEFINABLE:
            parameter['last_name'] = self._data.last_name

        try:
            self.Dut.sim.dut_simulator.add_author(**parameter)
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data_item: SingleDataItem,
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(f"DutSimulator.add_author() missing 1 required positional argument: '{without_mandatory_field}'")])

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
