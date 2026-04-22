import balder

import balderhub.data.lib.setup_features.factories
import balderhub.crud.lib.setup_features.factories

from tests.lib.setup_features.data import author
from tests.lib.utils.data_items import AuthorDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class SetupTriangleAuthor(balder.Setup):
    """
    Triangle setup for :class:`ScenarioTriangleSingleCreate` and :class:`ScenarioTriangleSingleUpdate` on the author
    data item. The DUT simulator is assigned to the ``PointOfTruth`` device. The ``Writer`` (combining create and
    update capabilities) and ``Reader`` devices access the simulator through their own features which map a VDevice
    to ``PointOfTruth``.
    """

    class PointOfTruth(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(
            AuthorDataItem
        )()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Writer(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            AuthorDataItem
        )(Master='PointOfTruth')
        creator = author.SingleAuthorCreator(Dut='PointOfTruth')
        create_example = author.ExampleCreateAuthorProvider()
        updater = author.SingleAuthorUpdator(Dut='PointOfTruth')
        single_example = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(
            AuthorDataItem, return_style='first'
        )()
        update_example = author.ExampleUpdateAuthorFieldProvider()

    @balder.connect(PointOfTruth, over_connection=balder.Connection)
    class Reader(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(
            AuthorDataItem
        )(Master='PointOfTruth')
        list_reader = author.MultipleAuthorReader(Dut='PointOfTruth')

    @balder.fixture('testcase')
    def setup_environment(self):
        self.PointOfTruth.env.sync_environment()
        yield
        self.PointOfTruth.sim.dut_simulator.clean_database()
