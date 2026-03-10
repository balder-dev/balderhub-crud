import dataclasses

from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature


class BaseFieldExampleProvider(AbstractDataItemRelatedFeature):
    """
    This config feature provides information for fields of data item elements of its specific data item type.
    """

    @dataclasses.dataclass
    class NamedExample:
        """internal data class that describes an example"""
        name: str

        def __str__(self):
            return f"FieldValueExample<{self.name}>"

    def get_valid_new_value_for_field(self, field: str) -> list[NamedExample]:
        """
        This method returns valid example data for a specific field of an existing data item instance. This will be
        called for change requests of a specific field of an existing data item.

        :param field: the field name that should be changed
        :return: the new value for the field
        """
        raise NotImplementedError

    def get_invalid_new_value_for_field(self, field: str) -> list[NamedExample]:
        """
        This method returns invalid example data for a specific field of an existing data item instance. This will be
        called for change requests of a specific field of an existing data item. It will be expected, that it is not
        possible to set the provided value in the app-under-test.

        :param field: the field name that should be changed
        :return: the new value for the field
        """
        raise NotImplementedError
