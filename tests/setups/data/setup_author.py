import balder

import balderhub.data.lib.setup_features.factories

from tests.lib.setup_features.data import author
from tests.lib.utils.data_items import AuthorDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature

class SetupAuthor(balder.Setup):

    class Dut(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        single_data = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(AuthorDataItem)()
        multiple_data = balderhub.data.lib.setup_features.factories.AutoMultipleDataConfigSetupFactory.get_for(AuthorDataItem)()

    @balder.connect(Dut, over_connection=balder.Connection)
    class Client(balder.Device):
        reader = author.SingleAuthorReader(Dut='Dut')
        multiple_reader = author.MultipleAuthorReader(Dut='Dut')
        creator = author.SingleAuthorCreator(Dut='Dut')
        updator = author.SingleAuthorUpdator(Dut='Dut')
        deleter = author.SingleAuthorDeleter(Dut='Dut')
        example = author.ExampleAuthorProvider()
        field_example = author.ExampleAuthorFieldModificationValueProvider()


    @balder.fixture('testcase')
    def setup_environment(self):
        self.Dut.env.setup_environment()
        yield
        self.Dut.sim.dut_simulator.clean_database()