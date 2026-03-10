from typing import Any

import balder
import balderhub.data

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.BookCategoryDataItem)
class SingleCategoryReader(SingleReaderFeature):

    class Dut(balder.VDevice):
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self, unique_identification_value: Any):
        category = self.Dut.dut.dut_simulator.get_category(unique_identification_value)
        self._loaded_data = {
            'id': category.id,
            'name': category.name,
        }

    def get_element_container(self) -> data_items.BookCategoryDataItem:
        return self._loaded_data

    def item_mapping(self) -> dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDictCallback(),
            'name': GrabFromDictCallback(),
        }
