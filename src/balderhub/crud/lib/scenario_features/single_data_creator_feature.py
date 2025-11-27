from typing import Any
from balderhub.crud.lib.scenario_features.single_data_filler_feature import SingleDataFillerFeature


class SingleDataCreatorFeature(SingleDataFillerFeature):
    """
    Scenario Feature that creates a new data item in the system-under-test.
    """
    # TODO do we consider an difference between a default value and a optional value??

    def get_expected_default_values_for_fields(self) -> dict[str, Any]:
        """
        :return: returns a dictionary of expected default values for fields in the system-under-test.
        """
        # TODO integrate check by comparing it with `Optional[]` types of data item definition
        return {}

    @property
    def resolved_fields_with_default_values(self) -> list[str]:
        """
        :return: a full resolved list of fields that have default values (means: if there is no value given with this
                 creator feature, it expects that the default value (specified within
                 :meth:`SingleDataCreatorFeature.get_expected_default_values_for_fields`) is set
        """
        result = []
        for cur_field_str, cur_default_value in self.get_expected_default_values_for_fields().items():
            # make sure that the default value is a string or integer or float or bool
            expected_default_value_types = (str, int, float, bool)
            if not isinstance(cur_default_value, expected_default_value_types):
                raise TypeError(f"expected default value for lookup field `{cur_field_str}` is in "
                                f"{expected_default_value_types}")
            result.append(cur_field_str)
        return result

    @property
    def resolved_mandatory_fields(self) -> list[str]:
        result = super().resolved_mandatory_fields
        return list(set(result) - set(self.resolved_fields_with_default_values))
