from typing import Dict

import balder
import balderhub.data

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleDataReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dataitem_callback import GrabFromDataitemCallback


@balderhub.data.register_for_data_item(data_items.BookCategoryDataItem)
class SingleCategoryReader(SingleDataReaderFeature):

    class Dut(balder.VDevice):
        single = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(data_items.BookCategoryDataItem)()
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self):
        categories = self.Dut.dut.dut_simulator.get_all_categories()
        self._loaded_data = [category for category in categories if category.get_unique_identification() == self.Dut.single.data_item.get_unique_identification()][0]

    def get_element_container(self) -> data_items.BookCategoryDataItem:
        return self._loaded_data

    # todo we have this double -> should we separate them from class?
    def _cb_get_from_data_item(self, field: str):
        return getattr(self._loaded_data, field)

    def item_mapping(self) -> Dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDataitemCallback(),
            'name': GrabFromDataitemCallback(),
        }
