from balderhub.data.lib.utils import SingleDataItem


class BookCategoryDataItem(SingleDataItem):
    id: int
    name: str

    def get_unique_identification(self):
        return self.id
