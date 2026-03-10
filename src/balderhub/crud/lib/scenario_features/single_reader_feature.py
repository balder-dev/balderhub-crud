from typing import Any
from balderhub.data.lib.utils import SingleDataItem

from balderhub.crud.lib.scenario_features.base_collector_feature import BaseCollectorFeature


class SingleReaderFeature(BaseCollectorFeature):
    """
    Scenario Feature that reads one data items from the system-under-test.
    """

    def load(self, unique_identification_value: Any):
        """
        Loads the system-under-test to be in the state for collecting the data item.
        """
        raise NotImplementedError

    def collect(self) -> SingleDataItem:
        """
        Executes the collecting process of the data item.
        :return: the collected data item
        """
        raise NotImplementedError()
