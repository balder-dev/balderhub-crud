from typing import Any

import balder

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback, Nested

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class SingleBookReader(SingleReaderFeature):

    class Dut(balder.VDevice):
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self, unique_identification_value: Any):
        book = self.Dut.dut.dut_simulator.get_book(unique_identification_value)
        author = self.Dut.dut.dut_simulator.get_author(book.author__id)
        category = self.Dut.dut.dut_simulator.get_category(book.category__id)
        self._loaded_data = {
            'id': book.id,
            'title': book.title,
            'author__id': author.id,
            'author__first_name': author.first_name,
            'author__last_name': author.last_name,
            'category__id': category.id,
            'category__name': category.name,
        }

    def get_element_container(self) -> data_items.BookDataItem:
        return self._loaded_data

    def item_mapping(self) -> dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDictCallback(),
            'title': GrabFromDictCallback(),
            'author': Nested(
                id=GrabFromDictCallback(),
                first_name=GrabFromDictCallback(),
                last_name=GrabFromDictCallback(),
            ),
            'category': Nested(
                id=GrabFromDictCallback(),
                name=GrabFromDictCallback(),
            )
        }
