import balder
from balderhub.data.lib.scenario_features import SingleDataConfig
from balderhub.crud.lib.scenario_features.single_data_reader_feature import SingleDataReaderFeature


class ScenarioSingleRead(balder.Scenario):
    """
    Comparing test scenario that validates if a specific single data item is collectable with the
    :class:`SingleDataReaderFeature`.
    """
    class PointOfTruth(balder.Device):
        """point of truth - holds the specific data item"""
        data = SingleDataConfig()  # TODO accessible like in `ScenarioListCompare`: should it be moved to DUT?

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        """the device under test at which we can read the specific data item"""
        reader = SingleDataReaderFeature()

    def test_compare_data(self):
        """
        This is a simple comparing test. It reads a specific data item with its :class:`SingleDataReaderFeature` and
        compares it with the expected data provided through :class:`SingleDataConfig`.

        The expected result is, that all collectable data fields are identically with the expected data items.
        """
        self.DeviceUnderTest.reader.load()

        pot_data = self.PointOfTruth.data.data_item
        device_data = self.DeviceUnderTest.reader.collect()

        compare_result = pot_data.get_difference_error_messages(
            device_data,
            ignore_field_lookups=self.DeviceUnderTest.reader.resolved_non_collectable_fields,
            allow_non_definable=True  # TODO do we want to allow NOT_DEFINABLE here?
        )
        assert not compare_result, f"compare function returns issues: {compare_result}"
