from balderhub.data.lib.scenario_features.data_environment_feature import DataEnvironmentFeature
from tests.lib.utils import data_items
from tests.lib.setup_features.dut_simulator_feature import DutSimulatorFeature


class TestDataEnvironment(DataEnvironmentFeature):

    sim = DutSimulatorFeature()

    def load_data(self):

        self._add_data(data_items.AuthorDataItem(1, 'J.K.', 'Rowling'))
        self._add_data(data_items.AuthorDataItem(2, 'J.R.R.', 'Tolkien'))
        self._add_data(data_items.AuthorDataItem(3, 'A.B.C.', 'Alphabet'))

        self._add_data(data_items.BookCategoryDataItem(1, 'Fantasy'))
        self._add_data(data_items.BookCategoryDataItem(2, 'Science Fiction'))
        self._add_data(data_items.BookCategoryDataItem(3, 'Action'))

        self._add_data(data_items.BookDataItem(
            1, 'Harry Potter and the Sorcerer’s Stone',
            author=self.get(data_items.AuthorDataItem, 1),
            category=self.get(data_items.BookCategoryDataItem, 1))
        )

        self._add_data(data_items.BookDataItem(
            2, 'Harry Potter and the Order of the Phoenix',
            author=self.get(data_items.AuthorDataItem, 1),
            category=self.get(data_items.BookCategoryDataItem, 1))
        )

        self._add_data(data_items.BookDataItem(
            3, 'The Hobbit',
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
