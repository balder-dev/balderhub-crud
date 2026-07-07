from __future__ import annotations

import copy
import dataclasses
from typing import Any, Dict, NamedTuple, Optional

from balderhub.data.lib.utils import NOT_DEFINABLE

from balderhub.crud.lib.utils import UNSET


class DutSimulator:
    @dataclasses.dataclass
    class Author:
        id: int
        first_name: str
        last_name: str

    @dataclasses.dataclass
    class Category:
        id: int
        name: str

    @dataclasses.dataclass
    class Book:
        id: int
        title: str
        author__id: int
        category__id: Optional[int] = None

    def __init__(self):
        self._all_authors: dict[int, DutSimulator.Author] = dict()
        self._all_categories: dict[int, DutSimulator.Category] = dict()
        self._all_books: dict[int, DutSimulator.Book] = dict()

    def _is_non_empty_string(self, elem):
        return isinstance(elem, str) and len(elem) > 0

    def _is_valid_integer_gt_1(self, elem):
        return isinstance(elem, int) and elem >= 1

    def add_author(self, first_name: str, last_name: str) -> None:
        if not self._is_non_empty_string(first_name):
            raise ValueError('The author needs a first name.')
        if not self._is_non_empty_string(last_name):
            raise ValueError('The author needs a last name.')

        new_id = 1 if len(self._all_authors) == 0 else max(self._all_authors.keys()) + 1
        self._all_authors[new_id] = self.Author(id=new_id, first_name=first_name, last_name=last_name)

    def get_author(self, by_id: int) -> Author:
        if by_id not in self._all_authors.keys():
            raise KeyError(f'unknown key id `{by_id}`')
        return self._all_authors[by_id]

    def update_in_author(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        author = self._all_authors[with_id]

        if 'first_name' in data_to_update and not self._is_non_empty_string(data_to_update['first_name']):
            raise ValueError('The author needs a first name.')
        if 'last_name' in data_to_update and not self._is_non_empty_string(data_to_update['last_name']):
            raise ValueError('The author needs a last name.')

        for cur_key in data_to_update.keys():
            if not cur_key in ['first_name', 'last_name']:
                raise KeyError(f'unknown key `{cur_key}`')

        for cur_field in data_to_update:
            setattr(author, cur_field, data_to_update[cur_field])

    def delete_author(self, author_id: int) -> None:

        if author_id in [book.author__id for book in self._all_books.values()]:
            raise ReferenceError('one or multiple Book objects referencing this author')

        del self._all_authors[author_id]

    def add_category(self, name: str) -> None:
        if not self._is_non_empty_string(name):
            raise ValueError('The category needs a name.')

        new_id = 1 if len(self._all_categories) == 0 else max(self._all_categories.keys()) + 1
        self._all_categories[new_id] = self.Category(id=new_id, name=name)

    def get_category(self, by_id: int) -> Category:
        if by_id not in self._all_categories.keys():
            raise KeyError(f'unknown key id `{by_id}`')
        return self._all_categories[by_id]

    def update_in_category(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        category = self._all_categories[with_id]

        if 'name' in data_to_update and not self._is_non_empty_string(data_to_update['name']):
            raise ValueError('The category needs a name.')

        for cur_key in data_to_update.keys():
            if not cur_key in ['name']:
                raise KeyError(f'unknown key `{cur_key}`')

        for cur_field in data_to_update:
            setattr(category, cur_field, data_to_update[cur_field])

    def delete_category(self, category_id: int) -> None:
        if category_id in [book.category_id for book in self._all_books.values()]:
            raise ReferenceError('one or multiple Book objects referencing this Category')

        del self._all_categories[category_id]

    def add_book(self, title: str, author: dict, category: Optional[dict] = None):
        if not self._is_non_empty_string(title):
            raise ValueError('The book needs a title.')

        if author in [None, NOT_DEFINABLE, UNSET]:
            raise ValueError('The book needs an author.')
        if not isinstance(author, dict):
            raise TypeError('The author needs to be a dict.')
        if 'id' not in author.keys():
            raise TypeError('The author needs to have a key `id`.')
        if author['id'] not in self._all_authors.keys():
            raise ValueError('The author is not known - you need to create it first')

        if category is not None and category not in [NOT_DEFINABLE, UNSET]:
            if not isinstance(category, dict):
                raise TypeError('The category needs to be a dict.')
            if 'id' not in category.keys():
                raise TypeError('The category needs to have a key `id`.')
            if category['id'] not in self._all_categories.keys():
                raise ValueError('The category is not known - you need to create it first')
        if category == UNSET:
            category = None

        new_id = 1 if len(self._all_books) == 0 else max(self._all_books.keys()) + 1
        self._all_books[new_id] = self.Book(
            id=new_id,
            title=title,
            author__id=author['id'],
            category__id=category['id'] if category else None
        )

    def get_book(self, by_id: int) -> Book:
        if by_id not in self._all_books.keys():
            raise KeyError(f'unknown key id `{by_id}`')
        return self._all_books[by_id]

    def update_in_book(self, with_id: int, data_to_update: Dict[str, Any]) -> None:
        book = self._all_books[with_id]

        if 'title' in data_to_update and not self._is_non_empty_string(data_to_update['title']):
            raise ValueError('The book needs a title.')
        if 'author' in data_to_update:
            if data_to_update['author'] in [None, NOT_DEFINABLE, UNSET]:
                raise ValueError('The book needs an author.')
            if not isinstance(data_to_update['author'], dict):
                raise TypeError('Author needs to be provided as dictionary')
            if data_to_update['author']['id'] not in self._all_authors.keys():
                raise ValueError('The author is not known - you need to create it first')
        if 'category' in data_to_update:
            category = data_to_update['category']

            if category is not None and category not in [NOT_DEFINABLE, UNSET]:
                if not isinstance(category, dict):
                    raise TypeError('The category needs to be a dict.')
                if 'id' not in category.keys():
                    raise TypeError('The category needs to have a key `id`.')
                if category['id'] not in self._all_categories.keys():
                    raise ValueError('The category is not known - you need to create it first')
            if category == UNSET:
                data_to_update['category'] = None

        cleaned_data_to_update = {}
        for cur_key in data_to_update.keys():
            if cur_key == 'title':
                cleaned_data_to_update[cur_key] = data_to_update[cur_key]
            elif cur_key  == 'author':
                cleaned_data_to_update["author__id"] = data_to_update[cur_key]['id']
            elif cur_key == 'category':
                cleaned_data_to_update["category__id"] = data_to_update[cur_key]['id'] if data_to_update[cur_key] else None
            else:
                raise KeyError(f'unknown key `{cur_key}`')

        for cur_field in cleaned_data_to_update:
            setattr(book, cur_field, cleaned_data_to_update[cur_field])

    def delete_book(self, book_id: int) -> None:
        del self._all_categories[book_id]

    def get_all_authors(self):
        return copy.deepcopy(list(self._all_authors.values()))

    def get_all_categories(self):
        return copy.deepcopy(list(self._all_categories.values()))

    def get_all_books(self):
        return copy.deepcopy(list(self._all_books.values()))

    def clean_database(self):
        self._all_authors = {}
        self._all_categories = {}
        self._all_books = {}
