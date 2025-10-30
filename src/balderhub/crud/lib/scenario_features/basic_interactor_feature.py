from balderhub.data.lib.utils.abstract_data_item_related_feature import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils.response_message_list import ResponseMessageList


class BasicInteractorFeature(AbstractDataItemRelatedFeature):

    def get_active_success_messages(self) -> ResponseMessageList:
        raise NotImplementedError()

    def get_active_error_messages(self) -> ResponseMessageList:
        raise NotImplementedError()
