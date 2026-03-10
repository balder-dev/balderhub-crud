import balder
import balderhub.data

from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback, Nested

import balderhub.crud.lib.setup_features

from ...dut_simulator_feature import DutSimulatorFeature
from ....utils import data_items
from ....utils.grab_from_dict_callback import GrabFromDictCallback


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class MultipleBookReader(balderhub.crud.lib.setup_features.MultipleReaderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elements = None

    def load(self):
        self._elements = []
        for cur_book in self.Dut.sim.dut_simulator.get_all_books():
            author = self.Dut.sim.dut_simulator.get_author(cur_book.author__id)
            category = self.Dut.sim.dut_simulator.get_category(cur_book.category__id)
            self._elements.append({
                'id': cur_book.id,
                'title': cur_book.title,
                'author__id': author.id,
                'author__first_name': author.first_name,
                'author__last_name': author.last_name,
                'category__id': category.id,
                'category__name': category.name,
            })

    def get_list_item_element_container(self) -> list[data_items.BookDataItem]:
        return self._elements

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
