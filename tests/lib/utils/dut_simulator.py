from __future__ import annotations
from typing import Any, Dict

from balderhub.data.lib.utils import NOT_DEFINABLE
from balderhub.data.lib.utils.single_data_item_collection import SingleDataItemCollection

from tests.lib.utils.data_items import AuthorDataItem, BookCategoryDataItem, BookDataItem


class DutSimulator:

    def __init__(self):
        self._all_authors = SingleDataItemCollection([])
        self._all_categories = SingleDataItemCollection([])
        self._all_books = SingleDataItemCollection([])

    def add_author(self, first_name: str, last_name: str) -> None:
        if first_name in '':
            raise ValueError('The author needs a first name.')
        if last_name == '':
            raise ValueError('The author needs a last name.')

        new_id = 1 if len(self._all_authors) == 0 else max([author.id for author in self._all_authors]) + 1
        self._all_authors.append(AuthorDataItem(id=new_id, first_name=first_name, last_name=last_name))

    def update_in_author(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        author = self._all_authors.get_by_identifier(with_id)

        if 'first_name' in data_to_update and data_to_update['first_name'] == '':
            raise ValueError('The author needs a first name.')
        if 'last_name' in data_to_update and data_to_update['last_name'] == '':
            raise ValueError('The author needs a last name.')
        for cur_field in data_to_update:
            setattr(author, cur_field, data_to_update[cur_field])

    def delete_author(self, author_id: int) -> None:
        author = self._all_authors.get_by_identifier(author_id)
        self._all_authors.remove(author)

    def add_category(self, name: str) -> None:
        if name == '':
            raise ValueError('The category needs a name.')

        new_id = 1 if len(self._all_categories) == 0 else max([cat.id for cat in self._all_categories]) + 1
        self._all_categories.append(BookCategoryDataItem(id=new_id, name=name))

    def update_in_category(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        category = self._all_categories.get_by_identifier(with_id)
        if 'name' in data_to_update and data_to_update['name'] == '':
            raise ValueError('The category needs a name.')
        for cur_field in data_to_update:
            setattr(category, cur_field, data_to_update[cur_field])

    def delete_category(self, category_id: int) -> None:
        category = self._all_categories.get_by_identifier(category_id)
        self._all_categories.remove(category)

    def add_book(self, title: str, author__id: int, category__id: int):
        if title == '':
            raise ValueError('The book needs a title.')
        if author__id in [None, NOT_DEFINABLE]:
            raise ValueError('The book needs a author.')
        if author__id not in self._all_authors.get_all_unique_identifier():
            raise ValueError('The author is not known - you need to create it first')
        if category__id in [None, NOT_DEFINABLE]:
            raise ValueError('The book needs a category.')
        if category__id not in self._all_categories.get_all_unique_identifier():
            raise ValueError('The category is not known - you need to create it first')

        author = self._all_authors.get_by_identifier(author__id)
        category = self._all_categories.get_by_identifier(category__id)

        new_id = 1 if len(self._all_books) == 0 else max([book.id for book in self._all_books]) + 1
        self._all_books.append(BookDataItem(id=new_id, title=title, author=author, category=category))

    def update_in_book(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        book = self._all_books.get_by_identifier(with_id)

        data_to_update = data_to_update.copy()

        for cur_key in data_to_update.keys():
            if not cur_key in ['title', 'author__id', 'category__id']:
                raise KeyError(f'unknown key `{cur_key}`')

        if data_to_update.get('title', None) == '':
            raise ValueError('The book needs a title.')
        if 'author__id' in data_to_update:
            if data_to_update['author__id'] is None:
                raise ValueError('The book needs an author.')
            if data_to_update['author__id'] not in self._all_authors.get_all_unique_identifier():
                raise ValueError('The provided author does not exist.')
            else:
                data_to_update['author'] = self._all_authors.get_by_identifier(data_to_update['author__id'])
                del data_to_update['author__id']
        if 'category__id' in data_to_update:
            if data_to_update['category__id'] is None:
                raise ValueError('The book needs a category.')
            if data_to_update['category__id'] not in self._all_categories.get_all_unique_identifier():
                raise ValueError('The provided category does not exist.')
            else:
                data_to_update['category'] = self._all_categories.get_by_identifier(data_to_update['category__id'])
                del data_to_update['category__id']
        for cur_field in data_to_update:
            setattr(book, cur_field, data_to_update[cur_field])

    def delete_book(self, book_id: int) -> None:
        book = self._all_books.get_by_identifier(book_id)
        self._all_books.remove(book)

    def get_all_authors(self):
        return self._all_authors.copy()

    def get_all_categories(self):
        return self._all_categories.copy()

    def get_all_books(self):
        return self._all_books.copy()

    def clean_database(self):
        self._all_authors = SingleDataItemCollection([])
        self._all_categories = SingleDataItemCollection([])
        self._all_books = SingleDataItemCollection([])