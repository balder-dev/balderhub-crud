import balder
import balderhub.data


from balderhub.crud.lib.setup_features.multiple_data_reader_feature import MultipleDataReaderFeature
from balderhub.crud.lib.utils.field_callbacks import FieldCollectorCallback, Nested

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items
from tests.lib.utils.grab_from_dataitem_callback import GrabFromDataitemCallback


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class MultipleBookReader(MultipleDataReaderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elements = None

    def load(self):
        self._elements = self.Dut.sim.dut_simulator.get_all_books()

    def get_list_item_element_container(self) -> list[data_items.BookDataItem]:
        return self._elements

    def _cb_get_from_data_item(self, data_item: data_items.BookDataItem, field: str, subfield: str = None):
        value = getattr(data_item, field)
        if subfield is not None:
            return getattr(value, subfield)
        return value

    def item_mapping(self) -> dict[str, FieldCollectorCallback]:
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
