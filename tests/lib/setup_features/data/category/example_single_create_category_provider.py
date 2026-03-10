from __future__ import annotations

import balderhub.data
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList, ResponseMessage

import balderhub.crud.lib.scenario_features

from ....utils.data_items import BookCategoryDataItem

@balderhub.data.register_for_data_item(BookCategoryDataItem)
class ExampleSingleCreateCategoryProvider(balderhub.crud.lib.scenario_features.SingleCreateExampleProvider):

    def get_valid_examples(self):
        return [
            self.NamedExample(
                name='Simple Category',
                data_item=BookCategoryDataItem(id=NOT_DEFINABLE, name='Special'),
                expected_response_messages=ResponseMessageList([])
            )
        ]

    def get_invalid_examples(self):
        return [
            self.NamedExample(
                name='Category with empty name',
                data_item=BookCategoryDataItem(id=NOT_DEFINABLE, name=''),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(text='The category needs a name.')]
                )
            ),
        ]
