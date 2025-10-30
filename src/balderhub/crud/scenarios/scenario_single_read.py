import balder
from balderhub.data.lib.scenario_features import SingleDataConfig
from balderhub.crud.lib.scenario_features.single_data_reader_feature import SingleDataReaderFeature


class ScenarioSingleRead(balder.Scenario):

    class PointOfTruth(balder.Device):
        data = SingleDataConfig()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class DeviceUnderTest(balder.Device):
        reader = SingleDataReaderFeature()

    def test_compare_data(self):
        self.DeviceUnderTest.reader.load()

        pot_data = self.PointOfTruth.data.data_item
        device_data = self.DeviceUnderTest.reader.collect()

        compare_result = pot_data.get_difference_error_messages(
            device_data, ignore_fields=self.DeviceUnderTest.reader.resolved_non_collectable_fields, allow_non_definable=True) # TODO do we want to allow NOT_DEFINABLE here?
        assert not compare_result, f"compare function returns issues: {compare_result}"
