from balderhub.data.lib.utils import SingleDataItem, LookupFieldString

from balderhub.crud.lib.utils.field_callbacks import Nested
from balderhub.crud.lib.utils.field_callbacks.base_field_callback import BaseFieldCallback


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

def get_flatten_fields_from_item_mapping(
        item_mapping: dict[str, BaseFieldCallback],
) -> set[LookupFieldString]:
    """
    Extracts and flattens field strings from a given item mapping.

    This function recursively traverses the provided item mapping of field strings
    to their associated callback objects, collecting and flattening all relevant
    field strings into a single set. If a field string is mapped to a `Nested`
    callback, the function further processes the nested item mappings.

    :param item_mapping: The dictionary mapping field strings to their respective
                         `BaseFieldCallback` objects. If any field string is
                         mapped to a `Nested` callback, its `inner_item_mapping`
                         attributes will also be processed.
    :return: A set of `LookupFieldString` objects representing the flattened field
             strings extracted from the item mapping.
    :raises TypeError: If the provided `item_mapping` is not of type `dict`.
    """
    if not isinstance(item_mapping, dict):
        raise TypeError("item_mapping must be a dict")

    result = set()
    for field_str, callback in item_mapping.items():
        if isinstance(callback, Nested):
            sub_fields = get_flatten_fields_from_item_mapping(callback.inner_item_mapping)
            result.update([LookupFieldString(field_str, field) for field in sub_fields])
        else:
            result.add(LookupFieldString(field_str))
    return result

def validate_existence_of_item_mapping(
        item_mapping: dict[str, BaseFieldCallback],
        for_data_item_type: type[SingleDataItem]
) -> None:
    """
    Validate the existence of item mappings for a given data item type and its fields.

    This function ensures that the provided `item_mapping` dictionary is valid for
    the specified `for_data_item_type`. It checks whether the `item_mapping` keys
    correspond to valid fields within the data item type and validates nested
    mappings recursively if `Nested` callbacks are encountered. Errors are raised
    if invalid mappings are found.

    :param item_mapping: A dictionary mapping field names to their respective field
        callbacks. Ensures that each key corresponds to a valid field within the data
        item type and validates nested mappings as necessary.
    :param for_data_item_type: The data item type to validate the `item_mapping` against.
        Must be a subclass of SingleDataItem.
    :raises TypeError: If `item_mapping` is not a dictionary or if
        `for_data_item_type` is not a subclass of SingleDataItem.
    :raises TypeError: If a nested item's type is not a subclass of SingleDataItem.
    :raises KeyError: If a field name in the `item_mapping` does not correspond to
        a valid field in `for_data_item_type`.
    """
    if not isinstance(item_mapping, dict):
        raise TypeError("item_mapping must be a dict")
    if not issubclass(for_data_item_type, SingleDataItem):
        raise TypeError("for_data_item_type must be a subclass of SingleDataItem")

    for cur_field, cur_callback in item_mapping.items():
        if isinstance(cur_callback, Nested):
            # check everything for this sub element
            sub_type = for_data_item_type.get_field_data_type(cur_field)
            if not issubclass(sub_type, SingleDataItem):
                raise TypeError(f"the field `{cur_field}` has a {Nested.__name__}() callback, but is no single "
                                f"data item (has type {sub_type})")
            validate_existence_of_item_mapping(cur_callback.inner_item_mapping, sub_type)
        else:
            if cur_field not in for_data_item_type.get_all_fields_for(nested=False):
                raise KeyError(f'no field `{cur_field}` exists within data item {for_data_item_type}')


def validate_completeness_of_item_mapping(
        item_mapping: dict[str, BaseFieldCallback],
        for_data_item_type: type[SingleDataItem],
        resolved_except_fields: set[LookupFieldString] | list[LookupFieldString],
) -> set[LookupFieldString]:
    """
    Validates the completeness of the item mapping for a given data item type. It ensures that
    all expected fields for the data item type, excluding the explicitly resolved exception
    fields, are covered in the item mapping. If a field or its parent field exists in
    the flattened item mapping, it is considered as accounted for.

    :param item_mapping: Dictionary mapping of fields to their associated `BaseFieldCallback`.
    :param for_data_item_type: The data item type for which the completeness check is performed.
    :param resolved_except_fields: A set or list of fields that should be excluded from
                                   the completeness validation as they are already resolved.
    :return: A set of `LookupFieldString` representing the missing fields that are not
             covered by the item mapping or resolved exception fields.
    """
    if not isinstance(item_mapping, dict):
        raise TypeError("item_mapping must be a dict")
    if not issubclass(for_data_item_type, SingleDataItem):
        raise TypeError("for_data_item_type must be a subclass of SingleDataItem")

    all_flatten_fields_from_item_mapping = get_flatten_fields_from_item_mapping(item_mapping)

    missing_fields = set()

    for expected_field in for_data_item_type.get_all_fields_for(nested=True):
        expected_field = LookupFieldString(expected_field)
        if expected_field in resolved_except_fields:
            continue
        #: in all other cases there needs to be an item_mapping for the field or for its parent field
        all_parent_fields = [
            LookupFieldString(*expected_field.split_field_keys[:-cnt])
            for cnt in range(1, len(expected_field.split_field_keys))
        ]
        for cur_field in [expected_field] + all_parent_fields:
            if cur_field in all_flatten_fields_from_item_mapping:
                # is available as item mapping -> done
                break
        else:
            missing_fields.add(expected_field)
    return missing_fields
