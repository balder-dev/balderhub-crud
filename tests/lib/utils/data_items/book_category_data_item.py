import balderhub.data.lib.utils.decorator_dataitem

from balderhub.data.lib.utils import SingleDataItem


@balderhub.data.lib.utils.decorator_dataitem.dataitem
class BookCategoryDataItem(SingleDataItem):
    id: int
    name: str

    def get_unique_identification(self):
        return self.id
