from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_field_value_provider_feature import ExampleFieldValueProviderFeature

from tests.lib.utils import data_items


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class ExampleBookFieldValueProvider(ExampleFieldValueProviderFeature):

    def get_valid_new_value_for_field(self, data_item: data_items.BookDataItem, field: str) -> Any:
        if field == 'title':
            return [
                self.NamedExample(
                    name="Changed Title",
                    field_name=field,
                    new_field_value='Hobbit'
                )
            ]
        if field == 'author__id':
            return [
                self.NamedExample(
                    name="Changed Author",
                    field_name=field,
                    new_field_value=3
                )
            ]
        if field == 'category__id':
            return [
                self.NamedExample(
                    name="Changed Category",
                    field_name=field,
                    new_field_value=3
                )
            ]
        return []

    def get_invalid_new_value_for_field(self, data_item: data_items.BookDataItem, field: str) -> Any:
        if field == 'title':
            return [
                self.NamedExample(
                    name="Empty Title",
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The book needs a title.')]
                    )
                )
            ]

        if field == 'author__id':
            return [
                self.NamedExample(
                    name="Empty Author",
                    field_name=field,
                    new_field_value=None,
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The book needs an author.')]
                    )
                ),
                self.NamedExample(
                    name='Author that does not exist',
                    field_name=field,
                    new_field_value=9999999,
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The provided author does not exist.')]
                    )
                ),
            ]

        if field == 'category__id':
            return [
                self.NamedExample(
                    name="Empty Category",
                    field_name=field,
                    new_field_value=None,
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The book needs a category.')]
                    )
                ),
                self.NamedExample(
                    name="Category that does not exist",
                    field_name=field,
                    new_field_value=9999999,
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The provided category does not exist.')]
                    )
                )
            ]
        return []