from __future__ import annotations
from typing import List

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList
from balderhub.data.lib.utils.functions import field_contained_in

from balderhub.crud.lib.scenario_features.basic_interactor_feature import BasicInteractorFeature


class SingleDataFillerFeature(BasicInteractorFeature):
    """
    Base scenario feature for filling a single data item.
    """

    def get_non_fillable_fields(self) -> List[str]:
        """
        This method should return a list of field names that are not fillable with this feature. Note that the method
        will assign the ``NOT_DEFINABLE`` object to the filled-field object.

        You can provide lookup strings for this field too. If the field is a nested data item, the feature will
        automatically resolve the nested fields.

        :return: returns a list of fields that are not collectable with this feature
        """
        return []

    def get_optional_fields(self) -> List[str]:
        """
        This method returns a list of field names that are optional.

        You can provide lookup strings for this field too. If the field is a nested data item, the feature will
        automatically resolve the nested fields.

        :return: returns a list of fields that are not collectable with this feature
        """
        result = []
        for cur_field in self.data_item_type.get_all_fields_for(nested=True):
            _, is_optional = self.data_item_type.get_field_data_type(cur_field)
            if is_optional:
                result.append(cur_field)
        return result

    def is_non_fillable_field(self, field_lookup: str) -> bool:
        """
        Checks if the provided field lookup string is a non-collectable field

        :param field_lookup: the field lookup to check
        :return: True if it is non-collectable, False otherwise
        """
        # TODO do we need this method for MANDATORY/OPTIONAL/FILLABLE too?
        field = self.data_item_type.get_field(field_lookup)
        return field_contained_in(field=field, list_of_resolved_field=self.resolved_non_fillable_fields)

    @property
    def resolved_non_fillable_fields(self) -> List[str]:
        """
        :return: a full resolved list of fields that are not fillable with this feature
        """
        result = []
        for subkey in self.get_non_fillable_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        return result

    @property
    def resolved_fillable_fields(self) -> List[str]:
        """
        :return: a full resolved list of fields that are fillable with this feature
        """
        return list(set(self.data_item_type.get_all_fields_for()) - set(self.resolved_non_fillable_fields))

    @property
    def resolved_mandatory_fields(self) -> List[str]:
        """
        :return: a full resolved list of fields that needs to be provided (means: if there is no value given with this
                 creator feature, it expects that there will be an error)
        """
        return list(set(self.resolved_fillable_fields) - set(self.resolved_optional_fields))

    @property
    def resolved_optional_fields(self) -> List[str]:
        """
        :return: a full resolved list of fields that optionally (means: if there is no value given with this
                 filler feature, it will not result into an error)
        """
        result = []
        for subkey in self.get_optional_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        # do only return fields that are fillable todo do we want that like this?
        result = list(set(result) - set(self.resolved_non_fillable_fields))

        # now make sure that the provided value OR its higher field lookups are OPTIONAL - at least one in the chain
        # needs to be optional
        for subkey in result:
            real_optional_field = subkey
            while True:
                # check if this sub-field can be optional
                _, is_optional = self.data_item_type.get_field_data_type(real_optional_field)
                if is_optional:
                    # passed
                    break
                cut_idx = real_optional_field.rfind("__")
                if cut_idx == -1:
                    # the provided OPTIONAL field is not valid - According the data-item configuration neither the
                    # field lookup nor its higher field lookups are defined as OPTIONAL
                    raise ValueError(f'invalid optional field lookup {subkey} for `{self.data_item_type}` detected - '
                                     f'this lookup or its higher chain elements are never defined as optional')
                real_optional_field = real_optional_field[:cut_idx]
        return result


    def get_expected_error_message_for_missing_mandatory_field(
            self,
            data_item: SingleDataItem,
            without_mandatory_field: str
    ) -> ResponseMessageList:
        """
        This method returns a list of expected error messages if one mandatory field is missing.
        :param data_item: the invalid data item that is filled
        :param without_mandatory_field: the mandatory field that is missing.
        :return: a list of expected error messages
        """
        raise NotImplementedError

    def load(self):
        """
        Loads the system-under-test to be in the state for filling the data item.
        """
        raise NotImplementedError

    def fill(self, data_class: SingleDataItem):
        """
        This method fills all the data of the provided data class
        :param data_class: the value providing data class that should be filled in
        :return: todo
        """
        raise NotImplementedError()

    def save(self):
        """
        This method executes the final submit command to trigger the saving of the filled data items
        :return:
        """
        raise NotImplementedError()
