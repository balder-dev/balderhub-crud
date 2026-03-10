from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage
import balderhub.crud.lib.scenario_features
import balderhub.crud.lib.setup_features
from ....utils.data_items import BookCategoryDataItem


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class ExampleSingleUpdateCategoryFieldProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):

    read_example = balderhub.crud.lib.scenario_features.factories.AutoSingleReadExampleFactory.get_for(BookCategoryDataItem)()

    def get_valid_new_value_for_field(self, field: str) -> Any:
        return [
            self.NamedExample(
                name="Changed Name",
                data_item=self.read_example.get_first_valid_example().data_item,
                field_name=field,
                new_field_value='Speciale'
            )
        ]

    def get_invalid_new_value_for_field(self, field: str) -> Any:
        if field == 'name':
            return [
                self.NamedExample(
                    name="Empty Name",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The category needs a name.')]
                    )
                ),
            ]
        return []