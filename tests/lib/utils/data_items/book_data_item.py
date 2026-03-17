from typing import Optional

from balderhub.data.lib.utils import SingleDataItem
from tests.lib.utils.data_items.author_data_item import AuthorDataItem
from tests.lib.utils.data_items.book_category_data_item import BookCategoryDataItem


class BookDataItem(SingleDataItem):
    id: int
    title: str
    author: AuthorDataItem
    category: Optional[BookCategoryDataItem] = None

    def get_unique_identification(self):
        return self.id
