import balder

import balderhub.data.lib.setup_features.factories
import balderhub.crud.lib.setup_features.factories

from tests.lib.setup_features.data import author
from tests.lib.utils.data_items import AuthorDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature

class SetupAuthor(balder.Setup):

    class Dut(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        initial_data = balderhub.data.lib.setup_features.factories.AutoInitialDataConfigFactory.get_for(AuthorDataItem)()

    @balder.connect(Dut, over_connection=balder.Connection)
    class Client(balder.Device):
        accessible_data = balderhub.data.lib.setup_features.factories.AutoAccessibleInitialDataConfigFactory.get_for(AuthorDataItem)(Master='Dut')
        reader = author.SingleAuthorReader(Dut='Dut')
        multiple_reader = author.MultipleAuthorReader(Dut='Dut')
        creator = author.SingleAuthorCreator(Dut='Dut')
        updator = author.SingleAuthorUpdator(Dut='Dut')
        deleter = author.SingleAuthorDeleter(Dut='Dut')
        create_example = author.ExampleCreateAuthorProvider()
        read_example = balderhub.crud.lib.setup_features.factories.AutoSingleReadExampleFactory.get_for(AuthorDataItem, return_style='first')()
        update_example = author.ExampleUpdateAuthorFieldProvider()
        # TODO delete_example = balderhub.crud.lib.setup_features.factories.AutoSingleDeleteExampleFactory.get_for(AuthorDataItem, return_style='first')()


    @balder.fixture('testcase')
    def setup_environment(self):
        self.Dut.env.sync_environment()
        yield
        self.Dut.sim.dut_simulator.clean_database()
