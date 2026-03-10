import balder
import balderhub.data

from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback

import balderhub.crud.lib.setup_features


from ...dut_simulator_feature import DutSimulatorFeature
from ....utils import data_items
from ....utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.AuthorDataItem)
class MultipleAuthorReader(balderhub.crud.lib.setup_features.MultipleReaderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elements = None

    def load(self):
        self._elements = []
        for cur_author in self.Dut.sim.dut_simulator.get_all_authors():
            self._elements.append({
                'id': cur_author.id,
                'first_name': cur_author.first_name,
                'last_name': cur_author.last_name
            })

    def get_list_item_element_container(self) -> list[data_items.AuthorDataItem]:
        return self._elements

    def item_mapping(self) -> dict[str, FieldCollectorCallback]:
        return {
            'id': GrabFromDictCallback(),
            'first_name': GrabFromDictCallback(),
            'last_name': GrabFromDictCallback(),
        }
