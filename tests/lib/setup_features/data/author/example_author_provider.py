from __future__ import annotations
from typing import List

import balderhub.data
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList, ResponseMessage
from balderhub.data.lib.scenario_features.example_data_provider_feature import ExampleDataProviderFeature

from tests.lib.utils.data_items import AuthorDataItem


@balderhub.data.register_for_data_item(AuthorDataItem)
class ExampleAuthorProvider(ExampleDataProviderFeature):

    def get_valid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        return [
            self.NamedExample(
                name='Simple Author',
                data=AuthorDataItem(id=NOT_DEFINABLE, first_name='Sam', last_name='Miller'),
                expected_response_messages=ResponseMessageList([])
            )
        ]

    def get_invalid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        return [
            self.NamedExample(
                name='Author with empty first name',
                data=AuthorDataItem(id=NOT_DEFINABLE, first_name='', last_name='Miller'),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The author needs a first name.')]
                )
            ),
            self.NamedExample(
                name='Author with empty last name',
                data=AuthorDataItem(id=NOT_DEFINABLE, first_name='Sam', last_name=''),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The author needs a last name.')]
                )
            )
        ]
