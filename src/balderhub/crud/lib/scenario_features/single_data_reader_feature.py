from balderhub.data.lib.utils import SingleDataItem
from balderhub.data.lib.utils.functions import field_contained_in

from balderhub.crud.lib.scenario_features.basic_interactor_feature import BasicInteractorFeature


class SingleDataReaderFeature(BasicInteractorFeature):
    """
    Scenario Feature that reads one data items from the system-under-test.
    """

    def get_non_collectable_fields(self) -> list[str]:
        """
        This method should return a list of field names that are not collectable by this feature. Note that the method
        will assign the ``NOT_DEFINABLE`` object to them.

        You can provide lookup strings for this field too. If the field is a nested data item, the feature will
        automatically resolve the nested fields.

        :return: returns a list of fields that are not collectable with this feature
        """
        return []

    @property
    def resolved_non_collectable_fields(self) -> list[str]:
        """
        :return: a full resolved list of fields that are not collectable with this feature
        """
        result = []
        for subkey in self.get_non_collectable_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        return result

    @property
    def resolved_collectable_fields(self) -> list[str]:
        """
        :return: a full resolved list of fields that are collectable with this feature
        """
        return list(set(self.data_item_type.get_all_fields_for()) - set(self.resolved_non_collectable_fields))

    def is_non_collectable_field(self, field_lookup: str) -> bool:
        """
        Checks if the provided field lookup string is a non-collectable field
        :param field_lookup: the field lookup to check
        :return: True if it is non-collectable, False otherwise
        """
        field = self.data_item_type.get_field(field_lookup)
        return field_contained_in(field=field, list_of_resolved_field=self.resolved_non_collectable_fields)

    def load(self):
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
