from typing import Dict, Any

import balder

import balderhub.data.lib.setup_features.factories

from balderhub.crud.lib.setup_features import SingleReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items

from tests.lib.utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.AuthorDataItem)
class SingleAuthorReader(SingleReaderFeature):

    class Dut(balder.VDevice):
        dut = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loaded_data = None

    def load(self, unique_identification_value: Any):
        author = self.Dut.dut.dut_simulator.get_author(unique_identification_value)
        self._loaded_data = {
            'id': author.id,
            'first_name': author.first_name,
            'last_name': author.last_name,
        }

    def get_element_container(self) -> data_items.AuthorDataItem:
        return self._loaded_data

    def item_mapping(self) -> Dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDictCallback(),
            'first_name': GrabFromDictCallback(),
            'last_name': GrabFromDictCallback(),
        }
