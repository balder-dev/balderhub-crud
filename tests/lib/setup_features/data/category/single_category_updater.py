from __future__ import annotations
from typing import List, Dict, Union
import copy

import balder
import balderhub.data

from balderhub.data.lib.setup_features import factories
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage, NOT_DEFINABLE

from balderhub.crud.lib.setup_features import SingleDataUpdaterFeature
from balderhub.crud.lib.utils.field_callbacks import FieldFillerCallback

from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.utils.inject_into_dataitem_callback import InjectIntoDataitemCallback


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class SingleCategoryUpdator(SingleDataUpdaterFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()
        single_data = factories.AutoSingleDataConfigSetupFactory.get_for(BookCategoryDataItem)()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data: Union[BookCategoryDataItem, None] = None
        self._last_exception = None

    def load(self):
        self._data = copy.deepcopy(
            self.Dut.sim.dut_simulator.get_all_categories().get_by_identifier(self.Dut.single_data.data_item.id))

    def get_non_fillable_fields(self) -> List[str]:
        return ['id']

    def get_element_container(self) -> BookCategoryDataItem:
        return self._data

    def item_mapping(self) -> Dict[str, FieldFillerCallback]:
        return {
            'name': InjectIntoDataitemCallback()
        }

    def save(self):
        self._last_exception = None
        if self._data is None:
            raise ValueError("No filled data")

        data_to_update = {}
        for cur_field in self._data.get_all_fields_for():
            if cur_field in self.resolved_non_fillable_fields:
                continue
            cur_value = self._data.get_field_value(cur_field)
            if cur_value != NOT_DEFINABLE:
                data_to_update[cur_field] = cur_value

        try:
            self.Dut.sim.dut_simulator.update_in_category(with_id=self._data.id, data_to_update=data_to_update)
            self._data = None
        except Exception as e:
            self._last_exception = e

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList()

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList([ResponseMessage(self._last_exception.args[0])] if self._last_exception else [])
