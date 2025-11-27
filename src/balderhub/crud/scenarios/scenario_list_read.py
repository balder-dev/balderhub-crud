import balder
from balderhub.data.lib.scenario_features import AllMultipleDataConfig, AccessibleMultipleDataConfig
from balderhub.crud.lib.scenario_features.multiple_data_reader_feature import MultipleDataReaderFeature


class ScenarioListCompare(balder.Scenario):
    """
    Comparing test scenario that validates if accessible data is collectable with the
    :class:`MultipleDataReaderFeature`.
    """

    class PointOfTruth(balder.Device):
        """point of truth - holds all expected data"""
        data = AllMultipleDataConfig()

    @balder.connect('PointOfTruth', over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        """the device under test at which we can read the data list and specify the accessible data (f.e. because of
        permission restrictions or user-permission scoped data)"""
        accessible_data = AccessibleMultipleDataConfig()
        reader = MultipleDataReaderFeature()

    def test_compare_data(self):
        """
        This is a simple comparing test. It reads all visible with its :class:`MultipleDataReaderFeature` and
        compares it with the expected data provided through :class:`AccessibleMultipleDataConfig`.

        The expected result is, that all collectable data fields are identically with the expected data items.
        """
        self.DeviceUnderTest.reader.load()

        pot_data = self.DeviceUnderTest.accessible_data.data_list
        device_data = self.DeviceUnderTest.reader.collect()

        assert len(pot_data) == len(device_data), (f"got {len(pot_data)} elements in point of truth "
                                                   f"and {len(device_data)} elements for DUT")

        compare_result = pot_data.get_difference_error_messages(
            device_data,
            ignore_order=True,
            ignore_field_lookups=self.DeviceUnderTest.reader.resolved_non_collectable_fields,
            allow_non_definable=True  # TODO do we want to allow NOT_DEFINABLE here?
        )
        assert not compare_result, f"compare function returns issues: {compare_result}"
