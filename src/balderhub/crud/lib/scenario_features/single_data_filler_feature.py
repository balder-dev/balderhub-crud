from __future__ import annotations
from typing import List

from balderhub.data.lib.utils import SingleDataItem, ResponseMessageList
from balderhub.data.lib.utils.functions import field_contained_in

from balderhub.crud.lib.scenario_features.basic_interactor_feature import BasicInteractorFeature


class SingleDataFillerFeature(BasicInteractorFeature):

    def get_non_fillable_fields(self) -> List[str]:
        return []

    def get_optional_fields(self) -> List[str]:
        result = []
        for cur_field in self.data_item_type.get_all_fields_for(nested=True):
            _, is_optional = self.data_item_type.get_field_data_type(cur_field)
            if is_optional:
                result.append(cur_field)
        return result

    def is_non_fillable_field(self, field_lookup: str) -> bool:
        # TODO do we need this method for MANDATORY/OPTIONAL/FILLABLE too?
        field = self.data_item_type.get_field(field_lookup)
        return field_contained_in(field=field, list_of_resolved_field=self.resolved_non_fillable_fields)

    @property
    def resolved_non_fillable_fields(self) -> List[str]:
        result = []
        for subkey in self.get_non_fillable_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        return result

    @property
    def resolved_fillable_fields(self) -> List[str]:
        return list(set(self.data_item_type.get_all_fields_for()) - set(self.resolved_non_fillable_fields))

    @property
    def resolved_mandatory_fields(self) -> List[str]:
        return list(set(self.resolved_fillable_fields) - set(self.resolved_optional_fields))

    @property
    def resolved_optional_fields(self) -> List[str]:
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
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def fill(self, data_class: SingleDataItem):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()
