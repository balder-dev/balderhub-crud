import balder

import balderhub.data.lib.setup_features.factories
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage

import balderhub.crud.lib.scenario_features
import balderhub.crud.lib.scenario_features

from tests.lib.setup_features import DutSimulatorFeature
from tests.lib.utils.data_items import BookDataItem


@balderhub.data.register_for_data_item(BookDataItem)
class SingleBookDeleter(balderhub.crud.lib.scenario_features.SingleDeleterFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()

    #example_delete = balderhub.crud.lib.scenario_features.factories.AutoSingleDeleteExampleFactory.get_for(BookDataItem)()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_exception = None

    def load(self):
        pass

    def delete(self):
        self._last_exception = None

        try:
            self.Dut.sim.dut_simulator.delete_book(self.example_delete.get_valid_examples()[0])
        except Exception as e:
            self._last_exception = e

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
