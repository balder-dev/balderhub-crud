import balder

import balderhub.data.lib.setup_features.factories
import balderhub.crud.lib.setup_features.factories

from tests.lib.setup_features.data import category
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class SetupTriangleCategory(balder.Setup):
    """
    Triangle setup for :class:`ScenarioTriangleSingleCreate` and :class:`ScenarioTriangleSingleUpdate` on the category
    data item. The DUT simulator is assigned to the ``PointOfTruth`` device. The ``Writer`` (combining create and
    update capabilities) and ``Reader`` devices access the simulator through their own features which map a VDevice
    to ``PointOfTruth``.
    """

    class PointOfTruth(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(
            BookCategoryDataItem
        )()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Writer(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            BookCategoryDataItem
        )(Master='PointOfTruth')
        creator = category.SingleCategoryCreator(Dut='PointOfTruth')
        create_example = category.ExampleSingleCreateCategoryProvider()
        updater = category.SingleCategoryUpdator(Dut='PointOfTruth')
        single_example = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(
            BookCategoryDataItem, return_style='first'
        )()
        update_example = category.ExampleSingleUpdateCategoryFieldProvider()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Reader(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            BookCategoryDataItem
        )(Master='PointOfTruth')
        list_reader = category.MultipleCategoryReader(Dut='PointOfTruth')

    @balder.fixture('testcase')
    def setup_environment(self):
        self.PointOfTruth.env.sync_environment()
        yield
        self.PointOfTruth.sim.dut_simulator.clean_database()
