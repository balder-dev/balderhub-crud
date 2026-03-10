from typing import Any

import balder
import balderhub.data

from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

import balderhub.crud.lib.setup_features

from ...dut_simulator_feature import DutSimulatorFeature
from ....utils import data_items
from ....utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.BookCategoryDataItem)
class MultipleCategoryReader(balderhub.crud.lib.setup_features.MultipleReaderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elements = None

    def load(self):
        self._elements = []
        for cur_category in self.Dut.sim.dut_simulator.get_all_categories():
            self._elements.append({
                'id': cur_category.id,
                'name': cur_category.name
            })

    def get_list_item_element_container(self) -> list[dict[str, Any]]:
        return self._elements

    def item_mapping(self) -> dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDictCallback(),
            'name': GrabFromDictCallback(),
        }
