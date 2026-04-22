import copy

import balder
from balder import parametrization

from balderhub.data.lib.utils.functions import set_lookup_field_in_data_dict

from balderhub.crud.lib import scenario_features


class ScenarioTriangleSingleUpdate(balder.Scenario):
    """
    Updating test scenario that validates if field updates for a specific item are possible.
    """

    class PointOfTruth(balder.Device):
        """point of truth - holds all expected data"""
        # TODO do we need this device

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class Updater(balder.Device):
        """the device under test that can update a new data item"""
        #: can update a data set in the system under test
        updater = scenario_features.SingleUpdaterFeature()
        #: can select one of the existing entries
        single_example = scenario_features.SingleReadExampleProvider()
        #: provides example data for the selected entry
        example = scenario_features.SingleUpdateFieldExampleProvider()

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class Reader(balder.Device):
        """the device that can read the data item list"""
        #: reads all existing accessible data
        list_reader = scenario_features.MultipleReaderFeature()

    @balder.parametrize_by_feature(
        'cur_fillable_field', (Updater, 'updater', 'resolved_fillable_fields')
    )
    @balder.parametrize_by_feature(
        'valid_example', (Updater, 'example', 'get_valid_new_value_for_field'),
        parameter={
            'field': parametrization.Parameter('cur_fillable_field')
        }
    )
    def test_field_update_valid(
            self,
            cur_fillable_field: str,
            valid_example: scenario_features.SingleUpdateFieldExampleProvider.NamedExample
    ):
        """
        This test tries to update fields. It will be auto parametrized and executed for all updatable fields. It is
        multiple parametrized and will automatically be called once per field and per configured field value (provided
        by :meth:`SingleUpdateFieldExampleProvider.get_valid_new_value_for_field`)

        :param cur_fillable_field: the parametrized field that should be updated with this test run (provided by
                                   :meth:`SingleUpdaterFeature.resolved_fillable_fields`
        :param valid_example: the parametrized dependent field-value (provided by
                              :meth:`SingleUpdateFieldExampleProvider.get_valid_new_value_for_field`) for the
                              current field (provided with parameter `cur_fillable_field`)
        """
        pot_data = valid_example.data_item
        self.Reader.list_reader.load()
        all_items_before = self.Reader.list_reader.collect()
        all_items_before_copy = all_items_before.copy()
        item_to_update_in_before = all_items_before.get_by_identifier(pot_data.get_unique_identification())
        all_items_before_copy.remove(item_to_update_in_before)
        assert pot_data.compare(item_to_update_in_before, allow_non_definable=True)  # TODO allow Non-Definable here?

        new_expected_data = copy.deepcopy(pot_data)
        new_expected_data.set_field_value(cur_fillable_field, valid_example.new_field_value)

        data_to_fill = pot_data.__class__.create_non_definable()
        data_to_fill.set_field_value(cur_fillable_field, valid_example.new_field_value)

        self.Updater.updater.load(unique_identification_value=pot_data.get_unique_identification())
        self.Updater.updater.fill(data_to_fill.model_dump())
        self.Updater.updater.save()

        error_messages = self.Updater.updater.get_active_error_messages()
        assert not error_messages, f"detect the following unexpected error messages: {error_messages}"

        # now make sure that data is updated
        self.Reader.list_reader.load()
        all_items_after = self.Reader.list_reader.collect()
        all_items_after_copy = all_items_after.copy()

        item_to_update_in_after = all_items_after.get_by_identifier(pot_data.get_unique_identification())
        all_items_after_copy.remove(item_to_update_in_after)

        assert new_expected_data.compare(
            item_to_update_in_after,
            allow_non_definable=True   # TODO allow Non-Definable here?
        )

        assert all_items_before_copy.compare(all_items_after_copy)


    @balder.parametrize_by_feature(
        'unset_optional_field', (Updater, 'updater', 'get_optional_fields')
    )
    def test_unset_optional_field(self, unset_optional_field):
        """
        This test tries to UNSET an existing field that is marked as optional. It will be auto parametrized and
        executed for all optional fields (provided by :meth:`SingleUpdaterFeature.get_optional_fields`).

        :param unset_optional_field: parametrized optional field name (provided by
                                       :meth:`SingleUpdaterFeature.get_optional_fields`)
        """
        pot_data = self.Updater.single_example.get_first_valid_example().data_item
        self.Reader.list_reader.load()
        all_items_before = self.Reader.list_reader.collect()
        all_items_before_copy = all_items_before.copy()
        item_to_update_in_before = all_items_before.get_by_identifier(pot_data.get_unique_identification())
        all_items_before_copy.remove(item_to_update_in_before)
        assert pot_data.compare(item_to_update_in_before, allow_non_definable=True)  # TODO allow Non-Definable here?

        new_expected_data = copy.deepcopy(pot_data)
        new_expected_data.set_field_value(unset_optional_field, None)

        data_to_fill = pot_data.__class__.create_non_definable()
        data_to_fill.set_field_value(unset_optional_field, None)

        self.Updater.updater.load(unique_identification_value=pot_data.get_unique_identification())
        self.Updater.updater.fill(data_to_fill.model_dump())
        self.Updater.updater.save()

        error_messages = self.Updater.updater.get_active_error_messages()
        assert not error_messages, f"detect the following unexpected error messages: {error_messages}"

        # now make sure that data is updated
        self.Reader.list_reader.load()
        all_items_after = self.Reader.list_reader.collect()
        all_items_after_copy = all_items_after.copy()

        item_to_update_in_after = all_items_after.get_by_identifier(pot_data.get_unique_identification())
        all_items_after_copy.remove(item_to_update_in_after)

        assert new_expected_data.compare(
            item_to_update_in_after,
            allow_non_definable=True   # TODO allow Non-Definable here?
        )

        assert all_items_before_copy.compare(all_items_after_copy)


    @balder.parametrize_by_feature(
        'cur_fillable_field', (Updater, 'updater', 'resolved_fillable_fields')
    )
    @balder.parametrize_by_feature(
        'invalid_example', (Updater, 'example', 'get_invalid_new_value_for_field'),
        parameter={
            'field': parametrization.Parameter('cur_fillable_field')
        }
    )
    def test_field_update_invalid(
            self,
            cur_fillable_field: str,
            invalid_example: scenario_features.SingleUpdateFieldExampleProvider.NamedExample
    ):
        """
        This test tries to update fields with illegal field values. It will be expected that this is not possible and
        the device-under-tests provides an expected error message.

        This test will be auto parametrized and executed for all updatable fields. It is
        multiple parametrized and will automatically be called once per field and per configured field value (provided
        by :meth:`SingleUpdateFieldExampleProvider.get_invalid_new_value_for_field`)

        :param cur_fillable_field: the parametrized field that should be updated with this test run (provided by
                                   :meth:`SingleUpdaterFeature.resolved_fillable_fields`
        :param invalid_example: the parametrized dependent illegal field-value (provided by
                                 :meth:`SingleUpdateFieldExampleProvider.get_invalid_new_value_for_field`) for the
                                 current field (provided with parameter `cur_fillable_field`)
        """
        pot_data = invalid_example.data_item

        self.Reader.list_reader.load()
        all_items_before = self.Reader.list_reader.collect()
        all_items_before_copy = all_items_before.copy()
        item_to_update_in_before = all_items_before.get_by_identifier(pot_data.get_unique_identification())
        all_items_before_copy.remove(item_to_update_in_before)
        assert pot_data.compare(item_to_update_in_before, allow_non_definable=True)  # TODO allow Non-Definable here?

        data_to_fill = pot_data.__class__.create_non_definable().model_dump()
        set_lookup_field_in_data_dict(data_to_fill, cur_fillable_field, invalid_example.new_field_value)

        self.Updater.updater.load(unique_identification_value=pot_data.get_unique_identification())
        self.Updater.updater.fill(data_to_fill)
        self.Updater.updater.save()

        error_messages = self.Updater.updater.get_active_error_messages()
        assert invalid_example.expected_response_messages.compare(error_messages), \
            (f"expected error message(s) `{invalid_example.expected_response_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        # now make sure that data is updated
        self.Reader.list_reader.load()
        all_items_after = self.Reader.list_reader.collect()

        assert all_items_before.compare(all_items_after, allow_non_definable=True)  # TODO allow Non-Definable here?
