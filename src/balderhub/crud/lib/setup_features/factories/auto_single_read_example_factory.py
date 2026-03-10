from typing import Literal

from balderhub.data.lib.utils.auto_feature_factory import AutoFeatureFactory
from balderhub.data.lib.scenario_features import AbstractDataItemRelatedFeature
import balderhub.data.lib.scenario_features
from balderhub.data.lib.utils.single_data_item import SingleDataItem
from ... import scenario_features


class AutoSingleReadExampleFactory(AutoFeatureFactory):
    """
    Factory for creating data-item bounded setup-based config-feature :class:`AllMultipleDataConfig` by using the
    defined data within a :class:`DataEnvironmentFeature`.
    """

    @classmethod
    def get_for(
            cls,
            data_item_cls: type[SingleDataItem],
            return_style: Literal['first', 'last', 'random', 'all'] = 'first',
            **kwargs
    ) -> type[AbstractDataItemRelatedFeature]:
        return super(AutoSingleReadExampleFactory, cls).get_for(
            data_item_cls, return_style=return_style, **kwargs
        )

    @classmethod
    def _define_class(cls, data_item_cls: type[SingleDataItem], **kwargs):
        return_style = kwargs['return_style']

        class AutoSingleReadExample(scenario_features.factories.AutoSingleReadExampleFactory.get_for(data_item_cls)):
            """inner factory-created feature class"""

            accessible_data = \
                balderhub.data.lib.scenario_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
                    data_item_cls
                )()

            def get_valid_examples(self):
                """
                :return: returns one example determined by the given ` return_style ` parameter in the factory
                """
                data_item_collection = self.accessible_data.data_list
                if return_style == 'first':
                    return [
                        self.NamedExample(
                            name='First',
                            data_item=data_item_collection[0],
                        )]
                if return_style == 'last':
                    return [
                        self.NamedExample(
                            name='Last',
                            data_item=data_item_collection[-1],
                        )]
                if return_style == 'random':
                    return [
                        self.NamedExample(
                            name='Random Item',
                            data_item=data_item_collection.get_random(),
                        )]
                # else
                return [
                    self.NamedExample(
                        name=f'Item {cur_idx + 1}/{len(data_item_collection)}',
                        data_item=cur_item,
                    ) for cur_idx, cur_item in enumerate(data_item_collection)]

        return AutoSingleReadExample
