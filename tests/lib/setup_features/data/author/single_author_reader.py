from typing import Dict

import balder

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleDataReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items

from tests.lib.utils.grab_from_dataitem_callback import GrabFromDataitemCallback


@balderhub.data.register_for_data_item(data_items.AuthorDataItem)
class SingleAuthorReader(SingleDataReaderFeature):

    class Dut(balder.VDevice):
        single = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(data_items.AuthorDataItem)()
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self):
        authors = self.Dut.dut.dut_simulator.get_all_authors()
        self._loaded_data = [author for author in authors if author.get_unique_identification() == self.Dut.single.data_item.get_unique_identification()][0]

    def get_element_container(self) -> data_items.AuthorDataItem:
        return self._loaded_data

    def item_mapping(self) -> Dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDataitemCallback(),
            'first_name': GrabFromDataitemCallback(),
            'last_name': GrabFromDataitemCallback(),
        }
