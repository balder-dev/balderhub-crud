from __future__ import annotations
import dataclasses

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList

from balderhub.crud.lib.scenario_features import BaseExampleProvider


class BaseMultipleExampleProvider(BaseExampleProvider):
    """Base class for example provider features that returns a selection of elements at once"""
    # TODO implement

    @dataclasses.dataclass
    class NamedExampleItem:
        """inner element of a :class:`BaseMultipleExampleProvider.NamedExample`"""
        data_item: SingleDataItem

    @dataclasses.dataclass
    class NamedExample(BaseExampleProvider.NamedExample):
        """named example element returned by a multiple example provider feature"""
        name: str
        items: list[BaseMultipleExampleProvider.NamedExampleItem]
        expected_response_messages: ResponseMessageList = dataclasses.field(default_factory=ResponseMessageList)


    def get_valid_examples(self) -> list[NamedExample]:
        raise NotImplementedError
