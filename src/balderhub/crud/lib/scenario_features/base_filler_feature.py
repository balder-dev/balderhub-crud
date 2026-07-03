from __future__ import annotations
from typing import Any

from balderhub.data.lib.utils import ResponseMessageList, LookupFieldString

from .base_interactor_feature import BaseInteractorFeature
from ..utils.functions import get_all_fields_from


class BaseFillerFeature(BaseInteractorFeature):
    """
    Base scenario feature for filling fields of data items.
    """

    def get_non_fillable_fields(self) -> list[str]:
        """
        This method should return a list of field names that are not fillable with this feature. Note that the method
        will assign the ``NOT_DEFINABLE`` object to the filled-field object.

        You can provide lookup strings for this field too. If the field is a nested data item, the feature will
        automatically resolve the nested fields.

        :return: returns a list of fields that are not collectable with this feature
        """
        return []

    def get_mandatory_fields(self) -> list[LookupFieldString]:
        """
        This method returns a list of field names that are marked as non-optional.

        :return: returns a list of fields that are not optional
        """

        return [
            field for field in get_all_fields_from(self.data_item_type)
            if not self.data_item_type.is_optional_field(field, consider_upper_optionals_too=False)
        ]

    def get_optional_fields(self) -> list[LookupFieldString]:
        """
        This method returns a list of field names that are marked as optional.

        :return: returns a list of fields that are optional
        """

        return [
            field for field in get_all_fields_from(self.data_item_type)
            if self.data_item_type.is_optional_field(field, consider_upper_optionals_too=False)
        ]

    def is_non_fillable_field(self, field_lookup: str | LookupFieldString) -> bool:
        """
        Checks if the provided field lookup string is a non-collectable field

        :param field_lookup: the field lookup to check
        :return: True if it is non-collectable, False otherwise
        """
        return self.data_item_type.all_field_lookups_are_within(field_lookup, self.resolved_non_fillable_fields)

    @property
    def resolved_non_fillable_fields(self) -> list[str]:
        """
        :return: a full resolved list of fields that are not fillable with this feature
        """
        result = []
        for subkey in self.get_non_fillable_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        return result

    @property
    def resolved_fillable_fields(self) -> list[str]:
        """
        :return: a full resolved list of fields that are fillable with this feature
        """
        return list(set(self.data_item_type.get_all_fields_for()) - set(self.resolved_non_fillable_fields))

    @property
    def resolved_mandatory_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that needs to be provided (means: if there is no value given with this
                 creator feature, it expects that there will be an error)
        """
        return [field for field in self.get_mandatory_fields() if not self.is_non_fillable_field(field)]

    @property
    def resolved_optional_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that optionally (means: if there is no value given with this
                 filler feature, it will not result into an error)
        """
        return [field for field in self.get_optional_fields() if not self.is_non_fillable_field(field)]

    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data: dict[str, Any],
            without_mandatory_field: str
    ) -> ResponseMessageList:
        """
        This method returns a list of expected error messages if one mandatory field is missing.
        :param data: the invalid data item that was filled
        :param without_mandatory_field: the mandatory field that is missing.
        :return: a list of expected error messages
        """
        raise NotImplementedError
