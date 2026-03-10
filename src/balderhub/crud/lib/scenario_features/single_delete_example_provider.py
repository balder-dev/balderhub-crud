from .base_single_example_provider import BaseSingleExampleProvider


class SingleDeleteExampleProvider(BaseSingleExampleProvider):
    """
    Provides example selection of existing data items that should be deleted.
    """

    def get_valid_examples(self) -> list[BaseSingleExampleProvider.NamedExample]:
        raise NotImplementedError()
