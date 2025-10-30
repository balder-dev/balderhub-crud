import balder
from balderhub.data.lib.scenario_features import AllMultipleDataConfig, AccessibleMultipleDataConfig
from balderhub.crud.lib.scenario_features.multiple_data_reader_feature import MultipleDataReaderFeature


class ScenarioListCompare(balder.Scenario):


    class PointOfTruth(balder.Device):
        data = AllMultipleDataConfig()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        accessible_data = AccessibleMultipleDataConfig()
        reader = MultipleDataReaderFeature()

    def test_compare_data(self):
        self.DeviceUnderTest.reader.load()

        pot_data = self.DeviceUnderTest.accessible_data.data_list
        device_data = self.DeviceUnderTest.reader.collect()

        assert len(pot_data) == len(device_data), (f"got {len(pot_data)} elements in point of truth "
                                                   f"and {len(device_data)} elements for DUT")

        compare_result = pot_data.get_difference_error_messages(
            device_data, ignore_order=True, ignore_fields=self.DeviceUnderTest.reader.resolved_non_collectable_fields,
            allow_non_definable=True)  # TODO do we want to allow NOT_DEFINABLE here?
        assert not compare_result, f"compare function returns issues: {compare_result}"
