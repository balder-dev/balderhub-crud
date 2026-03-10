import dataclasses

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature


class BaseExampleProvider(AbstractDataItemRelatedFeature):
    """
    This config feature provides information for a single data item element of its specific data item type.
    """

    @dataclasses.dataclass
    class NamedExample:
        """internal data class that describes an example"""
        name: str

        def __str__(self):
            return f"Example<{self.name}>"

    def get_valid_examples(self) -> list[NamedExample]:
        """
        :return: returns a list of valid examples
        """
        raise NotImplementedError

    def get_first_valid_example(self) -> NamedExample:
        """
        This method returns the first valid example of the provided examples within `get_valid_examples`.
        :return: the first valid example defined within `get_valid_examples()`
        """
        all_examples = self.get_valid_examples()
        if len(all_examples) == 0:
            raise ValueError(f'the `{self.__class__.__name__}` needs to return at least one valid example within '
                             f'method `get_valid_examples`')
        return all_examples[0]
