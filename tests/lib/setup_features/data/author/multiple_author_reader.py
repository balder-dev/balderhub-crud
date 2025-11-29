from typing import List, Dict

import balder

import balderhub.data

from balderhub.crud.lib.setup_features.multiple_data_reader_feature import MultipleDataReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dataitem_callback import GrabFromDataitemCallback


@balderhub.data.register_for_data_item(data_items.AuthorDataItem)
class MultipleAuthorReader(MultipleDataReaderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elements = None

    def load(self):
        self._elements = self.Dut.sim.dut_simulator.get_all_authors()

    def get_list_item_element_container(self) -> List[data_items.AuthorDataItem]:
        return self._elements

    def item_mapping(self) -> Dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDataitemCallback(),
            'first_name': GrabFromDataitemCallback(),
            'last_name': GrabFromDataitemCallback(),
        }
