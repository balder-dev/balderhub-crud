from balderhub.data.lib.utils.auto_feature_factory import AutoFeatureFactory
from balderhub.data.lib.utils.single_data_item import SingleDataItem

from ..single_read_example_provider import SingleReadExampleProvider


class AutoSingleReadExampleFactory(AutoFeatureFactory):
    """
    Factory for creating data-item bounded scenario-based config-feature :class:`SingleReadExampleProvider`
    """

    @classmethod
    def _define_class(cls, data_item_cls: type[SingleDataItem], **kwargs) -> type[SingleReadExampleProvider]:

        class AutoSingleReadExampleProvider(SingleReadExampleProvider):
            """inner factory-created feature class"""

            def get_valid_examples(self) -> list[SingleReadExampleProvider.NamedExample]:
                raise NotImplementedError()

        return AutoSingleReadExampleProvider
