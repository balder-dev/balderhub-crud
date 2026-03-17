from __future__ import annotations
from typing import List, Dict, Union, Any

import balder
import balderhub.data

from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage

from balderhub.crud.lib.setup_features import SingleCreatorFeature
from balderhub.crud.lib.utils import UNSET
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback, Nested

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookDataItem
from tests.lib.utils.inject_into_dict_callback import InjectIntoDictCallback


@balderhub.data.register_for_data_item(BookDataItem)
class SingleBookCreator(SingleCreatorFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: Union[dict[str, Any], None] = None
        self._last_exception = None

    def load(self):
        self._data = {}

    def get_non_fillable_fields(self) -> List[str]:
        return [
            'id',
            *BookDataItem.get_all_fields_for('author', except_fields=['id']),
            *BookDataItem.get_all_fields_for('category', except_fields=['id']),
        ]

    def get_element_container(self) -> dict[str, Any]:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'title': InjectIntoDictCallback(),
            'author': Nested(
                id=InjectIntoDictCallback()
            ),
            'category': Nested(
                id=InjectIntoDictCallback(),
                _unset_callback=InjectIntoDictCallback()
            )
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        try:
            self.Dut.sim.dut_simulator.add_book(**{k: v for k, v in self._data.items() if v != UNSET})
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data: dict[str, Any],
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(
            f"DutSimulator.add_book() missing 1 required positional argument: '{without_mandatory_field}'")])

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
