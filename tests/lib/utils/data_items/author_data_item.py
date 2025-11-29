import balderhub.data.lib.utils.decorator_dataitem

from balderhub.data.lib.utils import SingleDataItem


@balderhub.data.lib.utils.decorator_dataitem.dataitem
class AuthorDataItem(SingleDataItem):
    id: int
    first_name: str
    last_name: str

    def get_unique_identification(self):
        return self.id