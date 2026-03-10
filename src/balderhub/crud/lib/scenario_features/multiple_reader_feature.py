from balderhub.data.lib.utils import SingleDataItemCollection

from .base_collector_feature import BaseCollectorFeature


class MultipleReaderFeature(BaseCollectorFeature):
    """
    Scenario Feature that reads a list of data items from the system-under-test.
    """

    def load(self) -> None:
        """
        Loads the system-under-test to be in the state for collecting the data items.
        """
        raise NotImplementedError

    def collect(self) -> SingleDataItemCollection:
        """
        Executes the collecting process of the data items.
        :return: the collected data items
        """
        raise NotImplementedError()
