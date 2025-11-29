from __future__ import annotations
from typing import List
import balder

import balderhub.data
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_data_provider_feature import ExampleDataProviderFeature

from tests.lib.setup_features.data_environment_feature import DataEnvironmentFeature
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature
from tests.lib.utils import data_items


@balderhub.data.register_for_data_item(data_items.BookDataItem)
class ExampleBookProvider(ExampleDataProviderFeature):

    class Dut(balder.VDevice):
        sim = DutSimulatorFeature()
        env = DataEnvironmentFeature()

    def get_valid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        author = self.Dut.env.get(data_items.AuthorDataItem, 1)
        category = self.Dut.env.get(data_items.BookCategoryDataItem, 1)
        return [
            self.NamedExample(
                name='Simple Book',
                data=data_items.BookDataItem(id=NOT_DEFINABLE, title='The Hobbit', author=author, category=category),
                expected_response_messages=ResponseMessageList([])
            )
        ]

    def get_invalid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        author = self.Dut.env.get(data_items.AuthorDataItem, 1)
        category = self.Dut.env.get(data_items.BookCategoryDataItem, 1)
        return [
            self.NamedExample(
                name='Book with empty title',
                data=data_items.BookDataItem(id=NOT_DEFINABLE, title='', author=author, category=category),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The book needs a title.')]
                )
            ),
            self.NamedExample(
                name='Book with an author that does not exist',
                data=data_items.BookDataItem(
                    id=NOT_DEFINABLE, title='The Hobbit', category=category,
                    author=data_items.AuthorDataItem(id=9999999, first_name=NOT_DEFINABLE, last_name=NOT_DEFINABLE)),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The author is not known - you need to create it first')]
                )
            ),
            self.NamedExample(
                name='Book without an author',
                data=data_items.BookDataItem(id=NOT_DEFINABLE, title='The Hobbit', author=NOT_DEFINABLE, category=category),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text="DutSimulator.add_book() missing 1 required positional argument: 'author__id'")]
                )
            ),
            self.NamedExample(
                name='Book with a category that does not exist',
                data=data_items.BookDataItem(id=NOT_DEFINABLE, title='The Hobbit', author=author,
                                             category=data_items.BookCategoryDataItem(id=999999, name=NOT_DEFINABLE)),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The category is not known - you need to create it first')]
                )
            ),
            self.NamedExample(
                name='Book without a category',
                data=data_items.BookDataItem(id=NOT_DEFINABLE, title='The Hobbit', author=author, category=NOT_DEFINABLE),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text="DutSimulator.add_book() missing 1 required positional argument: 'category__id'")]
                )
            )
        ]
