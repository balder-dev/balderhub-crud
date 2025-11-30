from __future__ import annotations
from typing import List, Dict, Union

import balder
import balderhub.data

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList, ResponseMessage, NOT_DEFINABLE

from balderhub.crud.lib.setup_features import SingleDataCreatorFeature
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback, Nested

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookDataItem
from tests.lib.utils.inject_into_dataitem_callback import InjectIntoDataitemCallback


@balderhub.data.register_for_data_item(BookDataItem)
class SingleBookCreator(SingleDataCreatorFeature):
    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: Union[BookDataItem, None] = None
        self._last_exception = None

    def load(self):
        self._data = BookDataItem(id=NOT_DEFINABLE, title=NOT_DEFINABLE, author=NOT_DEFINABLE, category=NOT_DEFINABLE)

    def get_non_fillable_fields(self) -> List[str]:
        return [
            'id',
            *BookDataItem.get_all_fields_for('author', except_fields=['id']),
            *BookDataItem.get_all_fields_for('category', except_fields=['id']),
        ]

    def get_element_container(self) -> BookDataItem:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'title': InjectIntoDataitemCallback(),
            'author': Nested(
                id=InjectIntoDataitemCallback()
            ),
            'category': Nested(
                id=InjectIntoDataitemCallback()
            )
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        parameter = {}
        if self._data.title != NOT_DEFINABLE:
            parameter['title'] = self._data.title
        if self._data.author != NOT_DEFINABLE and self._data.author.id != NOT_DEFINABLE:
            parameter['author__id'] = self._data.author.id
        if self._data.category != NOT_DEFINABLE and self._data.category.id != NOT_DEFINABLE:
            parameter['category__id'] = self._data.category.id

        try:
            self.Dut.sim.dut_simulator.add_book(**parameter)
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data_item: SingleDataItem,
            without_mandatory_field: str
    ) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(
            f"DutSimulator.add_book() missing 1 required positional argument: '{without_mandatory_field}'")])

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
