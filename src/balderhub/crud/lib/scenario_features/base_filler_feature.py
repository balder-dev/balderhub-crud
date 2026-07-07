from __future__ import annotations

import copy
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

        You can provide lookup strings for this field too.

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

    def is_fillable_field(self, field_lookup: str | LookupFieldString) -> bool:
        """
        Checks if the provided field lookup string is a fillable field

        :param field_lookup: the field lookup to check
        :return: True if it is fillable, False otherwise
        """
        return field_lookup in self.resolved_fillable_fields

    def is_non_fillable_field(self, field_lookup: str | LookupFieldString) -> bool:
        """
        Checks if the provided field lookup string is a non-fillable field

        :param field_lookup: the field lookup to check
        :return: True if it is non-fillable, False otherwise
        """
        return field_lookup in self.resolved_non_fillable_fields

    @property
    def resolved_non_fillable_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that are not fillable with this feature
        """
        all_existing_fields = self.data_item_type.get_all_fields_for(nested=True)

        specified_non_fillable_fields = []
        for subkey in self.get_non_fillable_fields():
            if subkey not in all_existing_fields:
                raise KeyError(f'the specified field `{subkey}` is not part of `{self.data_item_type.__name__}`')
            specified_non_fillable_fields.append(LookupFieldString(subkey))
        return specified_non_fillable_fields

    @property
    def resolved_fillable_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that are fillable with this feature
        """
        all_fields = self.data_item_type.get_all_fields_for(nested=True)
        result = [LookupFieldString(field) for field in all_fields]

        for field in self.resolved_non_fillable_fields:
            if self.data_item_type.all_field_lookups_are_within(field, all_fields):
                # it is completely in not fillable fields -> remove it from result list
                for elem in copy.copy(result):
                    if field.split_field_keys == elem.split_field_keys[:len(field.split_field_keys)]:
                        # this current element is the searched field or its child -> remove it from result list
                        result.remove(elem)
        return result

    @property
    def resolved_mandatory_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that needs to be provided (means: if there is no value given with this
                 creator feature, it expects that there will be an error)
        """
        return [field for field in self.get_mandatory_fields() if self.is_fillable_field(field)]

    @property
    def resolved_optional_fields(self) -> list[LookupFieldString]:
        """
        :return: a full resolved list of fields that optionally (means: if there is no value given with this
                 filler feature, it will not result into an error)
        """
        return [field for field in self.get_optional_fields() if self.is_fillable_field(field)]

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
