from balderhub.data.lib.utils import ResponseMessageList

from balderhub.crud.lib.scenario_features.base_interactor_feature import BaseInteractorFeature


class BaseCollectorFeature(BaseInteractorFeature):
    """
    Scenario Feature that reads field data of data items.
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
        return self.data_item_type.all_field_lookups_are_within(field_lookup, self.resolved_non_collectable_fields)

    def get_active_success_messages(self) -> ResponseMessageList:
        raise NotImplementedError()

    def get_active_error_messages(self) -> ResponseMessageList:
        raise NotImplementedError()
