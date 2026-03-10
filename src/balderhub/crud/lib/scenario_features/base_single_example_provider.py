import dataclasses

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList

from balderhub.crud.lib.scenario_features import BaseExampleProvider


class BaseSingleExampleProvider(BaseExampleProvider):
    """Base class for example provider features that returns a single element"""

    @dataclasses.dataclass
    class NamedExample(BaseExampleProvider.NamedExample):
        """helper dataclass to describe a single named example"""
        name: str
        data_item: SingleDataItem
        expected_response_messages: ResponseMessageList = ResponseMessageList()

    def get_valid_examples(self) -> list[NamedExample]:
        raise NotImplementedError()
