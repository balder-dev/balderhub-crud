from __future__ import annotations
from typing import Any

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList, ResponseMessage, NOT_DEFINABLE
import balderhub.crud.lib.scenario_features

from balderhub.crud.lib.utils import UNSET

from tests.lib.utils import data_items
from tests.lib.utils.data_items import AuthorDataItem, BookCategoryDataItem


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class ExampleUpdateBookFieldProvider(balderhub.crud.lib.scenario_features.SingleUpdateFieldExampleProvider):

    read_example = balderhub.crud.lib.scenario_features.factories.AutoSingleReadExampleFactory.get_for(data_items.BookDataItem)()

    def get_valid_new_value_for_field(self, field: str) -> Any:
        if field == 'title':
            return [
                self.NamedExample(
                    name="Changed Title",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value='Hobbit'
                )
            ]
        if field == 'author':
            return [
                self.NamedExample(
                    name="Changed Author",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value=AuthorDataItem(id=3, first_name=NOT_DEFINABLE, last_name=NOT_DEFINABLE),
                )
            ]
        if field == 'category':
            return [
                self.NamedExample(
                    name="Changed Category",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value=BookCategoryDataItem(id=3, name=NOT_DEFINABLE),
                ),
            ]
        return []

    def get_invalid_new_value_for_field(self, field: str) -> Any:
        if field == 'title':
            return [
                self.NamedExample(
                    name="Empty Title",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value='',
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The book needs a title.')]
                    )
                )
            ]

        if field == 'author':
            return [
                self.NamedExample(
                    name="Empty Author",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value=UNSET,
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The book needs an author.')]
                    )
                ),
                self.NamedExample(
                    name='Author that does not exist',
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value=dict(id=9999999),
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text='The author is not known - you need to create it first')]
                    )
                ),
            ]

        if field == 'category':
            return [
                self.NamedExample(
                    name="Category that does not exist",
                    data_item=self.read_example.get_first_valid_example().data_item,
                    field_name=field,
                    new_field_value=dict(id=9999999),
                    expected_response_messages=ResponseMessageList(
                        [ResponseMessage(text="The category is not known - you need to create it first")]
                    )
                )
            ]
        return []
