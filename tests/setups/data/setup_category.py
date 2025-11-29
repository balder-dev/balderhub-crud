import balder

import balderhub.data.lib.setup_features.factories

from tests.lib.setup_features.data import category
from tests.lib.utils.data_items import BookCategoryDataItem
from tests.lib.setup_features.data_environment_feature import TestDataEnvironment
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature

class SetupCategory(balder.Setup):

    class Dut(balder.Device):
        sim = DutSimulatorFeature()
        env = TestDataEnvironment()
        single_data = balderhub.data.lib.setup_features.factories.AutoSingleDataConfigSetupFactory.get_for(BookCategoryDataItem)()
        multiple_data = balderhub.data.lib.setup_features.factories.AutoMultipleDataConfigSetupFactory.get_for(BookCategoryDataItem)()

    @balder.connect(Dut, over_connection=balder.Connection)
    class Client(balder.Device):
        reader = category.SingleCategoryReader(Dut='Dut')
        multiple_reader = category.MultipleCategoryReader(Dut='Dut')
        creator = category.SingleCategoryCreator(Dut='Dut')
        updator = category.SingleCategoryUpdator(Dut='Dut')
        deleter = category.SingleCategoryDeleter(Dut='Dut')
        example = category.ExampleCategoryProvider()
        field_example = category.ExampleCategoryFieldValueProvider()

    @balder.fixture('testcase')
    def setup_environment(self):
        self.Dut.env.setup_environment()
        yield
        self.Dut.sim.dut_simulator.clean_database()