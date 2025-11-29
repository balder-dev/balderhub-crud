from __future__ import annotations
from typing import List

import balderhub.data
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_data_provider_feature import ExampleDataProviderFeature

from tests.lib.utils.data_items import BookCategoryDataItem

@balderhub.data.register_for_data_item(BookCategoryDataItem)
class ExampleCategoryProvider(ExampleDataProviderFeature):

    def get_valid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        return [
            self.NamedExample(
                name='Simple Category',
                data=BookCategoryDataItem(id=NOT_DEFINABLE, name='Special'),
                expected_response_messages=ResponseMessageList([])
            )
        ]

    def get_invalid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        return [
            self.NamedExample(
                name='Category with empty name',
                data=BookCategoryDataItem(id=NOT_DEFINABLE, name=''),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The category needs a name.')]
                )
            ),
        ]
