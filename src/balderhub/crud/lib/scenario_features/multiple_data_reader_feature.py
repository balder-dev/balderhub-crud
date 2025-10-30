from balderhub.data.lib.utils import SingleDataItemCollection
from balderhub.data.lib.utils.functions import field_contained_in

from .basic_interactor_feature import BasicInteractorFeature


class MultipleDataReaderFeature(BasicInteractorFeature):

    def get_non_collectable_fields(self) -> list[str]:
        return []

    @property
    def resolved_non_collectable_fields(self) -> list[str]:
        result = []
        for subkey in self.get_non_collectable_fields():
            result.extend(self.data_item_type.get_all_fields_for(subkey, nested=True))
        return result

    @property
    def resolved_collectable_fields(self) -> list[str]:
        return list(set(self.data_item_type.get_all_fields_for()) - set(self.resolved_non_collectable_fields))

    def is_non_collectable_field(self, field_lookup: str) -> bool:
        field = self.data_item_type.get_field(field_lookup)
        return field_contained_in(field=field, list_of_resolved_field=self.resolved_non_collectable_fields)

    def load(self):
        raise NotImplementedError

    def collect(self) -> SingleDataItemCollection:
        raise NotImplementedError()
