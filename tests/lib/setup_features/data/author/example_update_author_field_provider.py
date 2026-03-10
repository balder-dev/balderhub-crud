from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage
import balderhub.crud.lib.scenario_features

from .example_create_author_provider import ExampleCreateAuthorProvider
from ....utils.data_items import AuthorDataItem


@balderhub.data.register_for_data_item(AuthorDataItem)
class ExampleUpdateAuthorFieldProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):

    read_example = balderhub.crud.lib.scenario_features.factories.AutoSingleReadExampleFactory.get_for(AuthorDataItem)()

    def get_valid_new_value_for_field(self, field: str) -> Any:
        return [
            self.NamedExample(
                name="Changed Name",
                data_item=self.read_example.get_first_valid_example().data_item,
                field_name=field,
                new_field_value='Chalana'
            )
        ]

    def get_invalid_new_value_for_field(self, field: str) -> Any:
        if field == 'first_name':
            return [
                self.NamedExample(
                    name="Empty Firstname",
                    data_item=self.read_example.get_first_valid_example().data_item,
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
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The author needs a last name.')]
                    )
                )
            ]
        return []