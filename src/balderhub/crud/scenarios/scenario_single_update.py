import copy

import balder
from balder import parametrization

from balderhub.data.lib.scenario_features import SingleDataConfig, ExampleFieldValueProviderFeature
from balderhub.crud.lib.scenario_features.multiple_data_reader_feature import MultipleDataReaderFeature
from balderhub.crud.lib.scenario_features.single_data_updater_feature import SingleDataUpdaterFeature


class ScenarioSingleUpdate(balder.Scenario):
    """
    Updating test scenario that validates if field updates for a specific item are possible.
    """

    class PointOfTruth(balder.Device):
        """point of truth - holds all expected data"""
        data = SingleDataConfig()

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        """the device under test at which we can read the data list and update a specific data item (f.e. because of
        permission restrictions or user-permission scoped data)"""
        list_reader = MultipleDataReaderFeature()
        updater = SingleDataUpdaterFeature()
        example = ExampleFieldValueProviderFeature()

    @balder.parametrize_by_feature(
        'cur_fillable_field', (DeviceUnderTest, 'updater', 'resolved_fillable_fields')
    )
    @balder.parametrize_by_feature(
        'valid_field_value', (DeviceUnderTest, 'example', 'get_valid_new_value_for_field'),
        parameter={
            'data_item': parametrization.FeatureAccessSelector(PointOfTruth, 'data', 'data_item'),
            'field': parametrization.Parameter('cur_fillable_field')
        }
    )
    def test_field_update_valid(self, cur_fillable_field, valid_field_value):
        """
        This test tries to update fields. It will be auto parametrized and executed for all updatable fields. It is
        multiple parametrized and will automatically be called once per field and per configured field value (provided
        by :meth:`ExampleFieldValueProviderFeature.get_valid_new_value_for_field`)

        :param cur_fillable_field: the parametrized field that should be updated with this test run (provided by
                                   :meth:`SingleDataUpdaterFeature.resolved_fillable_fields`
        :param valid_field_value: the parametrized dependent field-value (provided by
                                  :meth:`ExampleFieldValueProviderFeature.get_valid_new_value_for_field`) for the
                                  current field (provided with parameter `cur_fillable_field`)
        """
        pot_data = self.PointOfTruth.data.data_item

        # todo we should make the list-check optional - move it into separate scenario!
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        all_items_before_copy = all_items_before.copy()
        item_to_update_in_before = all_items_before.get_by_identifier(pot_data.get_unique_identification())
        all_items_before_copy.remove(item_to_update_in_before)
        assert pot_data.compare(item_to_update_in_before, allow_non_definable=True)  # TODO allow Non-Definable here?

        new_expected_data = copy.deepcopy(pot_data)
        new_expected_data.set_field_value(cur_fillable_field, valid_field_value.new_field_value)

        data_to_fill = pot_data.__class__.create_non_definable()
        data_to_fill.set_field_value(cur_fillable_field, valid_field_value.new_field_value)

        self.DeviceUnderTest.updater.load()
        self.DeviceUnderTest.updater.fill(data_to_fill)
        self.DeviceUnderTest.updater.save()

        error_messages = self.DeviceUnderTest.updater.get_active_error_messages()
        assert not error_messages, f"detect the following unexpected error messages: {error_messages}"

        # now make sure that data is updated
        # todo we should make the list-check optional - move it into separate scenario!
        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        all_items_after_copy = all_items_after.copy()

        item_to_update_in_after = all_items_after.get_by_identifier(pot_data.get_unique_identification())
        all_items_after_copy.remove(item_to_update_in_after)

        assert new_expected_data.compare(
            item_to_update_in_after,
            allow_non_definable=True   # TODO allow Non-Definable here?
        )

        assert all_items_before_copy.compare(all_items_after_copy)


    @balder.parametrize_by_feature(
        'cur_fillable_field', (DeviceUnderTest, 'updater', 'resolved_fillable_fields')
    )
    @balder.parametrize_by_feature(
        'invalid_field_value', (DeviceUnderTest, 'example', 'get_invalid_new_value_for_field'),
        parameter={
            'data_item': parametrization.FeatureAccessSelector(PointOfTruth, 'data', 'data_item'),
            'field': parametrization.Parameter('cur_fillable_field')
        }
    )
    def test_field_update_invalid(
            self,
            cur_fillable_field,
            invalid_field_value: ExampleFieldValueProviderFeature.NamedExample
    ):
        """
        This test tries to update fields with illegal field values. It will be expected that this is not possible and
        the device-under-tests provides an expected error message.

        This test will be auto parametrized and executed for all updatable fields. It is
        multiple parametrized and will automatically be called once per field and per configured field value (provided
        by :meth:`ExampleFieldValueProviderFeature.get_invalid_new_value_for_field`)

        :param cur_fillable_field: the parametrized field that should be updated with this test run (provided by
                                   :meth:`SingleDataUpdaterFeature.resolved_fillable_fields`
        :param invalid_field_value: the parametrized dependent illegal field-value (provided by
                                  :meth:`ExampleFieldValueProviderFeature.get_invalid_new_value_for_field`) for the
                                  current field (provided with parameter `cur_fillable_field`)
        """
        pot_data = self.PointOfTruth.data.data_item

        # todo we should make the list-check optional - move it into separate scenario!
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        all_items_before_copy = all_items_before.copy()
        item_to_update_in_before = all_items_before.get_by_identifier(pot_data.get_unique_identification())
        all_items_before_copy.remove(item_to_update_in_before)
        assert pot_data.compare(item_to_update_in_before, allow_non_definable=True)  # TODO allow Non-Definable here?

        data_to_fill = pot_data.__class__.create_non_definable()
        data_to_fill.set_field_value(cur_fillable_field, invalid_field_value.new_field_value)

        self.DeviceUnderTest.updater.load()
        self.DeviceUnderTest.updater.fill(data_to_fill)
        self.DeviceUnderTest.updater.save()

        error_messages = self.DeviceUnderTest.updater.get_active_error_messages()
        assert invalid_field_value.expected_response_messages.compare(error_messages), \
            (f"expected error message(s) `{invalid_field_value.expected_response_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        # now make sure that data is updated
        # todo we should make the list-check optional - move it into separate scenario!
        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()

        assert all_items_before.compare(all_items_after, allow_non_definable=True)  # TODO allow Non-Definable here?
