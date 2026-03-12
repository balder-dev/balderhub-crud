from typing import Any
import dataclasses

from balderhub.data.lib.utils import ResponseMessageList, SingleDataItem

from balderhub.crud.lib.scenario_features.base_field_example_provider import BaseFieldExampleProvider


class SingleUpdateFieldExampleProvider(BaseFieldExampleProvider):
    """
    This feature provides example data for specific fields of a data item.
    """

    @dataclasses.dataclass
    class NamedExample(BaseFieldExampleProvider.NamedExample):
        """internal data class that describes an example"""
        name: str
        data_item: SingleDataItem
        field_name: str
        new_field_value: Any
        expected_response_messages: ResponseMessageList = dataclasses.field(default_factory=ResponseMessageList)

        def __str__(self):
            return f"FieldValueExample<{self.field_name}: {self.name}>"

    def get_valid_new_value_for_field(self, field: str) -> list[NamedExample]:
        raise NotImplementedError

    def get_invalid_new_value_for_field(self, field: str) -> list[NamedExample]:
        raise NotImplementedError
