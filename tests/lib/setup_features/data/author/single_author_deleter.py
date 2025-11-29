import balder

import balderhub.data.lib.setup_features.factories
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage

from balderhub.crud.lib.scenario_features.single_data_deleter_feature import SingleDataDeleterFeature

from tests.lib.setup_features import DutSimulatorFeature
from tests.lib.utils.data_items import AuthorDataItem


@balderhub.data.register_for_data_item(AuthorDataItem)
class SingleAuthorDeleter(SingleDataDeleterFeature):

    class Dut(balder.VDevice):
        single = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(AuthorDataItem)()
        sim = DutSimulatorFeature()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_exception = None

    def load(self):
        pass

    def delete(self):
        self._last_exception = None

        try:
            self.Dut.sim.dut_simulator.delete_author(self.Dut.single.data_item.id)
        except Exception as e:
            self._last_exception = e

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
