import balder

from balderhub.crud.lib import scenario_features


class ScenarioSingleRead(balder.Scenario):
    """
    Comparing test scenario that validates if a specific single data item is collectable with the
    :class:`SingleDataReaderFeature`.
    """
    class PointOfTruth(balder.Device):
        """point of truth - holds the specific data item"""
        # TODO do we need this device?

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        """the device under test at which we can read the specific data item"""
        #: allows to read the data for a single data item
        reader = scenario_features.SingleReaderFeature()
        #: provides example data for an element that should be read and verified
        example = scenario_features.SingleReadExampleProvider()

    @balder.parametrize_by_feature('valid_example', (DeviceUnderTest, 'example', 'get_valid_examples'))
    def test_compare_data(self, valid_example: scenario_features.SingleReadExampleProvider.NamedExample):
        """
        This is a simple comparing test. It reads a specific data item with its :class:`SingleDataReaderFeature` and
        compares it with the expected data provided through :class:`SingleDataConfig`.

        The expected result is, that all collectable data fields are identically with the expected data items.
        """
        self.DeviceUnderTest.reader.load(valid_example.data_item.get_unique_identification())

        device_data = self.DeviceUnderTest.reader.collect()

        compare_result = valid_example.data_item.get_difference_error_messages(
            device_data,
            ignore_field_lookups=self.DeviceUnderTest.reader.resolved_non_collectable_fields,
            allow_non_definable=True
        )
        assert not compare_result, f"compare function returns issues: {compare_result}"

    # TODO should we add tests that validates invalid items?
