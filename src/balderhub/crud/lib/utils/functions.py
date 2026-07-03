from balderhub.data.lib.utils import SingleDataItem, LookupFieldString


def get_all_fields_from(data_item_type: type[SingleDataItem]) -> set[LookupFieldString]:
    """
    Helper function to determine all fields (incl nested)
    :param data_item_type: from the given data item type
    :return: a list of lookup field strings
    """
    all_fields = set()
    for cur_field in data_item_type.get_all_fields_for(nested=False):
        lookup = LookupFieldString(cur_field)
        all_fields.add(lookup)

        field_type = data_item_type.get_field_data_type(lookup)
        if issubclass(field_type, SingleDataItem):
            all_rel_fields = get_all_fields_from(field_type)
            all_fields |= set(LookupFieldString(cur_field, elem) for elem in all_rel_fields)
    return all_fields
