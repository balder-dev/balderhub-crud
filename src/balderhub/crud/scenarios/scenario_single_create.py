import logging
import copy
import balder
from balderhub.data.lib.scenario_features import ExampleDataProviderFeature
from balderhub.data.lib.utils import NOT_DEFINABLE
from balderhub.crud.lib.scenario_features.multiple_data_reader_feature import MultipleDataReaderFeature
from balderhub.crud.lib.scenario_features.single_data_creator_feature import SingleDataCreatorFeature

logger = logging.getLogger(__name__)


class ScenarioSingleCreate(balder.Scenario):
    """
    Creating test scenario that creates a new element in the system-under-test. This test scenario is a two-devices
    scenario. The device-under-test reads the list of data and also creates the new data item. If you want to use a test
    scenario which splits this features into two separate devices, you can use the
    :class:`ScenarioSingleCreateTriangle`.
    """

    class PointOfTruth(balder.Device):
        """point of truth - holds all expected data"""
        # TODO does it need to define a feature that the element was not created before???

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        """the device under test at which we can create the data list and specify the accessible data (f.e. because of
        permission restrictions or user-permission scoped data)"""
        #: reads all existing accessible data
        list_reader = MultipleDataReaderFeature()
        #: can create a new data set in the system under test
        creator = SingleDataCreatorFeature()
        #: provides example data for a full new data item
        example = ExampleDataProviderFeature()

    @balder.parametrize_by_feature(
        'valid_example', (DeviceUnderTest, 'example', 'get_valid_examples')
    )
    def test_create_valid(self, valid_example: ExampleDataProviderFeature.NamedExample):
        """
        This test creates a new data item in the device-under-test and validates its creation. It checks all fillable
        and collectable data fields before and after the new data item was created. It makes sure that only one data
        with the correct field values was created.

        :param valid_example: parametrized valid example (provided by
                              :meth:`ExampleDataProviderFeature.get_valid_examples`)
        """
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        self.DeviceUnderTest.creator.fill(valid_example.data)
        self.DeviceUnderTest.creator.save()

        if valid_example.expected_response_messages:
            success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
            assert valid_example.expected_response_messages.compare(success_messages), \
                (f"expected success message(s) `{valid_example.expected_response_messages}` not detected "
                 f"(detected success message: `{success_messages}`)")

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        assert not error_messages, f"saw active error message(s): {error_messages}"

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(cur_item_after), \
                f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, "found more newly created elements"
        # also compare the new one
        assert valid_example.data.compare(copied_all_items_after[0],  allow_non_definable=True), \
            "found difference to expectation for newly created data item"

    @balder.parametrize_by_feature(
        'invalid_example', (DeviceUnderTest, 'example', 'get_invalid_examples')
    )
    def test_create_invalid(self, invalid_example: ExampleDataProviderFeature.NamedExample):
        """
        This test tries to create a new invalid data item in the device-under-test and makes sure that it was not
        created. It also validates that the correct error messages were returned by the system and that the previous
        existing data does not change during this failed-creation.

        :param invalid_example: the parametrized invalid example (provided by
                                :meth:`ExampleDataProviderFeature.get_invalid_examples`)
        """
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        self.DeviceUnderTest.creator.fill(invalid_example.data)
        self.DeviceUnderTest.creator.save()

        success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        assert not success_messages, f"detect unexpected active success message(s): {success_messages}"

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        assert invalid_example.expected_response_messages.compare(error_messages), \
            (f"expected error message(s) `{invalid_example.expected_response_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        # no item should be created
        assert len(all_items_before) == len(all_items_after)

        assert all_items_after.compare(all_items_before), "existing data has changed"

    @balder.parametrize_by_feature(
        'without_optional_field', (DeviceUnderTest, 'creator', 'resolved_optional_fields')
    )
    def test_create_valid_without_single_optional_field(self, without_optional_field: str):
        """
        This test creates a new data item in the device-under-test and validates its creation. It uses the first valid
        example provided by :meth:`ExampleDataProviderFeature.get_valid_examples`, but without one optional field given
        by `without_optional_field` (provided with :meth:`SingleDataCreatorFeature.resolved_optional_fields`. This is
        expected to run successfully without any error.
        The test checks that the data items before and after the creation don't change (all fillable and
        collectable data fields were checked here).
        It makes sure that only one data item and also with the correct field values was created.

        .. note::
            This test is an auto parametrized test. It uses dynamical parametrization and asks the setup feature version
            of :class:`SingleDataCreatorFeature` for all existing optional fields and performs the test for
            each optional field.

            It does this individually for each field. There is currently no scenario that does this with multiple
            optional fields at the same time. If you need such a test, you will have to implement it individually.

        .. note::
            At the moment this feature does not validate the optional field (the value will be set to `NOT_DEFINABLE`).

        :param without_optional_field: parametrized optional field name (provided by
                                       :meth:`SingleDataCreatorFeature.resolved_optional_fields`)
        """
        # TODO validate the optional field value - if it is empty or None?
        valid_example = self.DeviceUnderTest.example.get_valid_examples()[0]

        # now get the field that needs to be set to None
        #  NOTE: This can be a higher nested field, because the identifier of an object (f.e. the id) is a nested field
        #        of the object that is actually set to None. The method
        #        :meth:`SingleDataCreatorFeature.resolved_optional_fields` does only return the key that has a valid
        #        callback, but the optional field can be higher. -> We are looking forward the next higher field that
        #        can be optional!
        real_optional_field = without_optional_field
        while True:
            # check if this sub-field can be optional
            _, is_optional = valid_example.data.__class__.get_field_data_type(real_optional_field)
            if is_optional:
                logger.info(f'set `None` to field value `{real_optional_field}`, because this is the higher field that '
                            f'can be optional')
                break
            cut_idx = real_optional_field.rfind("__")
            if cut_idx == -1:
                # should never be called except the additional check in
                # :meth:`SingleDataCreatorFeature.resolved_optional_fields` was overwritten
                raise ValueError('invalid optional field detected - can not be None because it or higher fields are '
                                 'not optional')
            real_optional_field = real_optional_field[:cut_idx]


        expected_data = copy.deepcopy(valid_example.data)
        expected_data.set_field_value(
            real_optional_field,
            None,
            only_change_this_value=True
        )

        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        data_to_fill = copy.deepcopy(valid_example.data)
        data_to_fill.set_field_value(without_optional_field, NOT_DEFINABLE, only_change_this_value=True)

        self.DeviceUnderTest.creator.load()
        self.DeviceUnderTest.creator.fill(data_to_fill)
        self.DeviceUnderTest.creator.save()

        # TODO how should we validate the message?
        # if valid_example.expected_response_messages:
        #     success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        #     assert valid_example.expected_response_messages.compare(success_messages), \
        #         (f"expected success message(s) `{valid_example.expected_response_messages}` not detected "
        #          f"(detected success message: `{success_messages}`)")

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        assert not error_messages, f"saw active error message(s): {error_messages}"

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(cur_item_after), \
                f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, "found more newly created elements"
        # also compare the new one
        assert expected_data.compare(copied_all_items_after[0], allow_non_definable=True), \
            "found difference to expectation for newly created data item"


    @balder.parametrize_by_feature(
        'without_field', (DeviceUnderTest, 'creator', 'resolved_fields_with_default_values')
    )
    def test_create_valid_without_single_field_with_default_value(self, without_field: str):
        """
        This test creates a new data item in the device-under-test and validates its creation. It uses the first valid
        example provided by :meth:`ExampleDataProviderFeature.get_valid_examples`, but without one field given
        by `without_field` (provided with :meth:`SingleDataCreatorFeature.resolved_fields_with_default_values`. This is
        expected to run successfully without any error.

        The test checks that all fillable and collectable data fields before and after the new data item was created.
        It makes sure that only one data item and also with the correct field values was created. It also validates that
        the non-filled default value has the expected default value.

        .. note::
            This test is an auto parametrized test. It uses dynamical parametrization and asks the setup feature version
            of :class:`SingleDataCreatorFeature` for all existing fields with default values and performs the test for
            each field with a default value.

            It does this individually for each field. There is currently no scenario that does this with multiple
            fields at the same time. If you need such a test, you will have to implement it individually.

        :param without_field: parametrized optional field name (provided by
                              :meth:`SingleDataCreatorFeature.resolved_fields_with_default_values`)
        """
        valid_example = self.DeviceUnderTest.example.get_valid_examples()[0]

        expected_data = copy.deepcopy(valid_example.data)
        expected_data.set_field_value(
            without_field,
            # todo structure that nicer
            self.DeviceUnderTest.creator.get_expected_default_values_for_fields()[without_field],
            only_change_this_value=True
        )

        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        data_to_fill = copy.deepcopy(valid_example.data)
        data_to_fill.set_field_value(without_field, NOT_DEFINABLE, only_change_this_value=True)

        self.DeviceUnderTest.creator.load()
        self.DeviceUnderTest.creator.fill(data_to_fill)
        self.DeviceUnderTest.creator.save()

        # TODO how should we validate the message?
        # if valid_example.expected_response_messages:
        #     success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        #     assert valid_example.expected_response_messages.compare(success_messages), \
        #         (f"expected success message(s) `{valid_example.expected_response_messages}` not detected "
        #          f"(detected success message: `{success_messages}`)")

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        assert not error_messages, f"saw active error message(s): {error_messages}"

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(cur_item_after), \
                f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, "found more newly created elements"
        # also compare the new one
        assert expected_data.compare(copied_all_items_after[0], allow_non_definable=True), \
            "found difference to expectation for newly created data item"

    @balder.parametrize_by_feature(
        'without_mandatory_field', (DeviceUnderTest, 'creator', 'resolved_mandatory_fields')
    )
    def test_create_invalid_with_missing_mandatory_field(self, without_mandatory_field: str):
        """
        This test tries to create a new data item in the device-under-test without a mandatory field. It uses the first
        valid example provided by :meth:`ExampleDataProviderFeature.get_valid_examples`, but without one field given
        by `without_mandatory_field` (provided with :meth:`SingleDataCreatorFeature.resolved_mandatory_fields`. This is
        expected to result into an error, which will be also verified.

        The test checks that all fillable and collectable data fields before and after the failing creation is valid
        (does not change and no data item is added).

        .. note::
            This test is an auto parametrized test. It uses dynamical parametrization and asks the setup feature version
            of :class:`SingleDataCreatorFeature` for all existing mandatory fields and performs the test for
            each of these fields.

            It does this individually for each field. There is currently no scenario that does this with multiple
            fields at the same time. If you need such a test, you will have to implement it individually.

        :param without_mandatory_field: parametrized mandatory field name (provided by
                                        :meth:`SingleDataCreatorFeature.resolved_mandatory_fields`)
        """
        valid_example = self.DeviceUnderTest.example.get_valid_examples()[0]

        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        manipulated_data = copy.deepcopy(valid_example.data)
        manipulated_data.set_field_value(without_mandatory_field, NOT_DEFINABLE, only_change_this_value=True)

        filled_data_class = self.DeviceUnderTest.creator.fill(manipulated_data)
        self.DeviceUnderTest.creator.save()

        success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        assert not success_messages, f"detect unexpected active success message(s): {success_messages}"

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        expected_error_messages = self.DeviceUnderTest.creator.get_expected_error_message_for_missing_mandatory_field(
            filled_data_class, without_mandatory_field
        )
        assert expected_error_messages.compare(error_messages), \
            (f"expected error message(s) `{expected_error_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_elements()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        # no item should be created
        assert len(all_items_before) == len(all_items_after)

        assert all_items_after.compare(all_items_before), "existing data has changed"
