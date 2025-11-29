from typing import Dict, Union

import balder

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleDataReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback, Nested

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dataitem_callback import GrabFromDataitemCallback


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class SingleBookReader(SingleDataReaderFeature):

    class Dut(balder.VDevice):
        single = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(data_items.BookDataItem)()
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self):
        books = self.Dut.dut.dut_simulator.get_all_books()
        self._loaded_data = [book for book in books if book.get_unique_identification() == self.Dut.single.data_item.get_unique_identification()][0]

    # todo we have this double -> should we separate them from class?
    def _cb_get_from_data_item(self, field: str, subfield: Union[str, None] = None):
        value = getattr(self._loaded_data, field)
        if subfield is not None:
            return getattr(value, subfield)
        return value

    def get_element_container(self) -> data_items.BookDataItem:
        return self._loaded_data

    def item_mapping(self) -> Dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDataitemCallback(),
            'title': GrabFromDataitemCallback(),
            'author': Nested(
                id=GrabFromDataitemCallback(),
                first_name=GrabFromDataitemCallback(),
                last_name=GrabFromDataitemCallback(),
            ),
            'category': Nested(
                id=GrabFromDataitemCallback(),
                name=GrabFromDataitemCallback(),
            )
        }
