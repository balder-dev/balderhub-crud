from __future__ import annotations
from .base_interactor_feature import BaseInteractorFeature


class SingleDeleterFeature(BaseInteractorFeature):
    """
    Scenario Feature that deletes an existing data item in the system-under-test.
    """
    # TODO improve - different types of deleting

    def load(self):
        """
        Loads the system-under-test to be in the state for deleting the data item.
        """
        raise NotImplementedError

    def delete(self) -> None:
        """
        Executes the deleting of the data item.
        """
        raise NotImplementedError()
