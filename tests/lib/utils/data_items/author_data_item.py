from balderhub.data.lib.utils import SingleDataItem


class AuthorDataItem(SingleDataItem):
    id: int
    first_name: str
    last_name: str

    def get_unique_identification(self):
        return self.id