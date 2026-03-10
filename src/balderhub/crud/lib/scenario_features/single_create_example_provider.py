from .base_single_example_provider import BaseSingleExampleProvider


class SingleCreateExampleProvider(BaseSingleExampleProvider):
    """
    This feature provides full example data for a specific single data item.
    """

    def get_invalid_examples(self) -> list[BaseSingleExampleProvider.NamedExample]:
        """
        :return: returns a list of invalid examples
        """
        raise NotImplementedError
