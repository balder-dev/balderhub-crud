from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_field_value_provider_feature import ExampleFieldValueProviderFeature

from tests.lib.utils.data_items import AuthorDataItem


@balderhub.data.register_for_data_item(AuthorDataItem)
class ExampleAuthorFieldModificationValueProvider(ExampleFieldValueProviderFeature):

    def get_valid_new_value_for_field(self, data_item: AuthorDataItem, field: str) -> Any:
        return [
            self.NamedExample(
                name="Changed Name",
                field_name=field,
                new_field_value='Chalana'
            )
        ]

    def get_invalid_new_value_for_field(self, data_item: AuthorDataItem, field: str) -> Any:
        if field == 'first_name':
            return [
                self.NamedExample(
                    name="Empty Firstname",
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The author needs a first name.')]
                    )
                )
            ]

        if field == 'last_name':
            return [
                self.NamedExample(
                    name="Empty Lastname",
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The author needs a last name.')]
                    )
                )
            ]
