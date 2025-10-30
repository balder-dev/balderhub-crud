import logging
import balder
import copy
from balderhub.data.lib.scenario_features import ExampleDataProviderFeature
from balderhub.data.lib.utils import NOT_DEFINABLE
from balderhub.crud.lib.scenario_features.multiple_data_reader_feature import MultipleDataReaderFeature
from balderhub.crud.lib.scenario_features.single_data_creator_feature import SingleDataCreatorFeature

logger = logging.getLogger(__name__)


class ScenarioSingleCreate(balder.Scenario):

    class PointOfTruth(balder.Device):
        pass

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        list_reader = MultipleDataReaderFeature()
        creator = SingleDataCreatorFeature()
        example = ExampleDataProviderFeature()

    @balder.parametrize_by_feature('valid_example', (DeviceUnderTest, 'example', 'get_valid_examples'))
    def test_create_valid(self, valid_example: ExampleDataProviderFeature.NamedExample):
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        filled_data_class = self.DeviceUnderTest.creator.fill(valid_example.data)
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
        assert all_items_after.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(cur_item_after), f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, f"found more newly created elements"
        # also compare the new one
        assert valid_example.data.compare(copied_all_items_after[0],  allow_non_definable=True), f"found difference to expectation for newly created data item"

    @balder.parametrize_by_feature('invalid_example', (DeviceUnderTest, 'example', 'get_invalid_examples'))
    def test_create_invalid(self, invalid_example: ExampleDataProviderFeature.NamedExample):
        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        filled_data_class = self.DeviceUnderTest.creator.fill(invalid_example.data)
        self.DeviceUnderTest.creator.save()

        success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        assert not success_messages, f"detect unexpected active success message(s): {success_messages}"

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        assert invalid_example.expected_response_messages.compare(error_messages), \
            (f"expected error message(s) `{invalid_example.expected_response_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        # no item should be created
        assert len(all_items_before) == len(all_items_after)

        assert all_items_after.compare(all_items_before), f"existing data has changed"

    @balder.parametrize_by_feature('without_optional_field', (DeviceUnderTest, 'creator', 'resolved_optional_fields'))
    def test_create_valid_without_single_optional_field(self, without_optional_field: str):
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
        assert all_items_before.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        data_to_fill = copy.deepcopy(valid_example.data)
        data_to_fill.set_field_value(without_optional_field, NOT_DEFINABLE, only_change_this_value=True)

        self.DeviceUnderTest.creator.load()
        filled_data_class = self.DeviceUnderTest.creator.fill(data_to_fill)
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
        assert all_items_after.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(
                cur_item_after), f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, f"found more newly created elements"
        # also compare the new one
        assert expected_data.compare(copied_all_items_after[0], allow_non_definable=True), \
            f"found difference to expectation for newly created data item"


    @balder.parametrize_by_feature('without_field', (DeviceUnderTest, 'creator', 'resolved_fields_with_default_values'))
    def test_create_valid_without_single_field_with_default_value(self, without_field: str):
        valid_example = self.DeviceUnderTest.example.get_valid_examples()[0]

        expected_data = copy.deepcopy(valid_example.data)
        expected_data.set_field_value(
            without_field,
            self.DeviceUnderTest.creator.get_expected_default_values_for_fields()[without_field], # todo structure that nicer
            only_change_this_value=True
        )

        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        data_to_fill = copy.deepcopy(valid_example.data)
        data_to_fill.set_field_value(without_field, NOT_DEFINABLE, only_change_this_value=True)

        self.DeviceUnderTest.creator.load()
        filled_data_class = self.DeviceUnderTest.creator.fill(data_to_fill)
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
        assert all_items_after.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        assert len(all_items_before) == len(all_items_after) - 1

        copied_all_items_after = all_items_after.copy()

        for cur_item_before in all_items_before:
            cur_item_after = copied_all_items_after.get_by_identifier(cur_item_before.get_unique_identification())
            # make sure that values are the same
            assert cur_item_before.compare(
                cur_item_after), f"untouched item with identifier `{cur_item_before.get_unique_identification()}` has changed"
            copied_all_items_after.remove(cur_item_after)

        # now only the newly created one should remain
        assert len(copied_all_items_after) == 1, f"found more newly created elements"
        # also compare the new one
        assert expected_data.compare(copied_all_items_after[0], allow_non_definable=True), \
            f"found difference to expectation for newly created data item"

    @balder.parametrize_by_feature('without_mandatory_field', (DeviceUnderTest, 'creator', 'resolved_mandatory_fields'))
    def test_create_invalid_with_missing_mandatory_field(self, without_mandatory_field: str):
        valid_example = self.DeviceUnderTest.example.get_valid_examples()[0]

        self.DeviceUnderTest.list_reader.load()
        all_items_before = self.DeviceUnderTest.list_reader.collect()
        # make sure that all others identification values are NOT_DEFINABLE (in `all_items_before`)
        assert all_items_before.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_before.get_all_unique_identifier()

        self.DeviceUnderTest.creator.load()
        manipulated_data = copy.deepcopy(valid_example.data)
        manipulated_data.set_field_value(without_mandatory_field, NOT_DEFINABLE, only_change_this_value=True)

        filled_data_class = self.DeviceUnderTest.creator.fill(manipulated_data)
        self.DeviceUnderTest.creator.save()

        success_messages = self.DeviceUnderTest.creator.get_active_success_messages()
        assert not success_messages, f"detect unexpected active success message(s): {success_messages}"

        error_messages = self.DeviceUnderTest.creator.get_active_error_messages()
        expected_error_messages = self.DeviceUnderTest.creator.get_expected_error_message_for_missing_mandatory_field(filled_data_class, without_mandatory_field)
        assert expected_error_messages.compare(error_messages), \
            (f"expected error message(s) `{expected_error_messages}` not detected (detected "
             f"error message: `{error_messages}`)")

        self.DeviceUnderTest.list_reader.load()
        all_items_after = self.DeviceUnderTest.list_reader.collect()
        assert all_items_after.has_unique_identifier()
        assert NOT_DEFINABLE not in all_items_after.get_all_unique_identifier()

        # no item should be created
        assert len(all_items_before) == len(all_items_after)

        assert all_items_after.compare(all_items_before), f"existing data has changed"
