import balder

import balderhub.data.lib.setup_features.factories

from tests.lib.setup_features.data import book
from tests.lib.utils.data_items import BookDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class SetupBook(balder.Setup):

    class Dut(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        single_data = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(BookDataItem)()
        multiple_data = balderhub.data.lib.setup_features.factories.AutoMultipleDataConfigSetupFactory.get_for(BookDataItem)()

    @balder.connect(Dut, over_connection=balder.Connection)
    class Client(balder.Device):
        reader = book.SingleBookReader(Dut='Dut')
        multiple_reader = book.MultipleBookReader(Dut='Dut')
        creator = book.SingleBookCreator(Dut='Dut')
        updator = book.SingleBookUpdator(Dut='Dut')
        deleter = book.SingleBookDeleter(Dut='Dut')
        example = book.ExampleBookProvider(Dut='Dut')
        field_example = book.ExampleBookFieldValueProvider()

    @balder.fixture('testcase')
    def setup_environment(self):
        self.Dut.env.setup_environment()
        yield
        self.Dut.sim.dut_simulator.clean_database()