from __future__ import annotations
from typing import Any


from .base_filler_feature import BaseFillerFeature


class SingleFillerFeature(BaseFillerFeature):
    """
    Base scenario feature for filling a single data item.
    """

    def load(self, **kwargs) -> None:
        """
        Loads the system-under-test to be in the state for filling the data item.
        """
        raise NotImplementedError

    def fill(self, data_class_dict: dict[str, Any]) -> dict[str, Any]:
        """
        This method fills all the data of the provided data class
        :param data_class_dict: the values that should be filled in as a dictionary
        :return: a new data class with the data, that was filled in
        """
        raise NotImplementedError()

    def save(self) -> None:
        """
        This method executes the final submit command to trigger the saving of the filled data items
        :return:
        """
        raise NotImplementedError()
