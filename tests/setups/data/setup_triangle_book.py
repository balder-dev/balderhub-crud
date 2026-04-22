import balder

import balderhub.data.lib.setup_features.factories
import balderhub.crud.lib.setup_features.factories

from tests.lib.setup_features.data import book
from tests.lib.utils.data_items import BookDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class SetupTriangleBook(balder.Setup):
    """
    Triangle setup for :class:`ScenarioTriangleSingleCreate` and :class:`ScenarioTriangleSingleUpdate` on the book
    data item. The DUT simulator is assigned to the ``PointOfTruth`` device. The ``Writer`` (combining create and
    update capabilities) and ``Reader`` devices access the simulator through their own features which map a VDevice
    to ``PointOfTruth``.
    """

    class PointOfTruth(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(
            BookDataItem
        )()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Writer(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            BookDataItem
        )(Master='PointOfTruth')
        creator = book.SingleBookCreator(Dut='PointOfTruth')
        create_example = book.ExampleCreateBookProvider(Dut='PointOfTruth')
        updater = book.SingleBookUpdator(Dut='PointOfTruth')
        single_example = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(
            BookDataItem, return_style='first'
        )()
        update_example = book.ExampleUpdateBookFieldProvider()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Reader(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            BookDataItem
        )(Master='PointOfTruth')
        list_reader = book.MultipleBookReader(Dut='PointOfTruth')

    @balder.fixture('testcase')
    def setup_environment(self):
        self.PointOfTruth.env.sync_environment()
        yield
        self.PointOfTruth.sim.dut_simulator.clean_database()
