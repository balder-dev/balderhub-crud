from .base_single_example_provider import BaseSingleExampleProvider


class SingleReadExampleProvider(BaseSingleExampleProvider):
    """
    Provides example selection of existing data items that should be read.
    """

    def get_valid_examples(self) -> list[BaseSingleExampleProvider.NamedExample]:
        raise NotImplementedError()
