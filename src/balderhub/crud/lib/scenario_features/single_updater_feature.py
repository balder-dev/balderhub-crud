from typing import Any

from balderhub.crud.lib.scenario_features.single_filler_feature import SingleFillerFeature


class SingleUpdaterFeature(SingleFillerFeature):
    """
    Scenario Feature that updating a new data item in the system-under-test.
    """

    def load(self, unique_identification_value: Any, **kwargs):  # pylint: disable=arguments-differ
        """
        Loads the system-under-test to be in the state for filling the data item.
        """
        raise NotImplementedError
