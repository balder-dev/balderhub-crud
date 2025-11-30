from balderhub.data.lib.scenario_features.data_environment_feature import DataEnvironmentFeature
from tests.lib.utils import data_items
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class TestDataEnvironment(DataEnvironmentFeature):

    sim = DutSimulatorFeature()

    def load_data(self):

        self._add_data(data_items.AuthorDataItem(id=1, first_name='J.K.', last_name='Rowling'))
        self._add_data(data_items.AuthorDataItem(id=2, first_name='J.R.R.', last_name='Tolkien'))
        self._add_data(data_items.AuthorDataItem(id=3, first_name='A.B.C.', last_name='Alphabet'))

        self._add_data(data_items.BookCategoryDataItem(id=1, name='Fantasy'))
        self._add_data(data_items.BookCategoryDataItem(id=2, name='Science Fiction'))
        self._add_data(data_items.BookCategoryDataItem(id=3, name='Action'))

        self._add_data(data_items.BookDataItem(
            id=1, title='Harry Potter and the Sorcerer’s Stone',
            author=self.get(data_items.AuthorDataItem, 1),
            category=self.get(data_items.BookCategoryDataItem, 1))
        )

        self._add_data(data_items.BookDataItem(
            id=2, title='Harry Potter and the Order of the Phoenix',
            author=self.get(data_items.AuthorDataItem, 1),
            category=self.get(data_items.BookCategoryDataItem, 1))
        )

        self._add_data(data_items.BookDataItem(
            id=3, title='The Hobbit',
            author=self.get(data_items.AuthorDataItem, 2),
            category=self.get(data_items.BookCategoryDataItem, 1))
        )

    def setup_environment(self):
        for cur_author in self.get_all_for(data_items.AuthorDataItem):
            self.sim.dut_simulator._all_authors.append(cur_author)
        for cur_category in self.get_all_for(data_items.BookCategoryDataItem):
            self.sim.dut_simulator._all_categories.append(cur_category)
        for cur_book in self.get_all_for(data_items.BookDataItem):
            self.sim.dut_simulator._all_books.append(cur_book)
