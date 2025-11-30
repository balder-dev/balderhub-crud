from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_field_value_provider_feature import ExampleFieldValueProviderFeature

from tests.lib.utils.data_items import BookCategoryDataItem


@balderhub.data.register_for_data_item(BookCategoryDataItem)
class ExampleCategoryFieldValueProvider(ExampleFieldValueProviderFeature):

    def get_valid_new_value_for_field(self, data_item: BookCategoryDataItem, field: str) -> Any:
        return [
            self.NamedExample(
                name="Changed Name",
                field_name=field,
                new_field_value='Speciale'
            )
        ]

    def get_invalid_new_value_for_field(self, data_item: BookCategoryDataItem, field: str) -> Any:
        if field == 'name':
            return [
                self.NamedExample(
                    name="Empty Name",
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The category needs a name.')]
                    )
                )
            ]
        return []