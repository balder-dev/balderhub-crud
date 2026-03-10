import balder

import balderhub.data.lib.setup_features.factories
import balderhub.crud.lib.setup_features.factories

from tests.lib.setup_features.data import book
from tests.lib.utils.data_items import BookDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class SetupBook(balder.Setup):

    class Dut(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(BookDataItem)()

    @balder.connect(Dut, over_connection=balder.Connection)
    class Client(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(BookDataItem)(Master='Dut')
        reader = book.SingleBookReader(Dut='Dut')
        multiple_reader = book.MultipleBookReader(Dut='Dut')
        creator = book.SingleBookCreator(Dut='Dut')
        updator = book.SingleBookUpdator(Dut='Dut')
        deleter = book.SingleBookDeleter(Dut='Dut')
        create_example = book.ExampleCreateBookProvider(Dut='Dut')
        read_example = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(BookDataItem, return_style='first')()
        update_example = book.ExampleUpdateBookFieldProvider()
        # TODO delete_example = balderhub.crud.lib.setup_features.factories.AutoSingleDeleteExampleFactory.get_for(BookDataItem, return_style='first')()

    @balder.fixture('testcase')
    def setup_environment(self):
        self.Dut.env.sync_environment()
        yield
        self.Dut.sim.dut_simulator.clean_database()