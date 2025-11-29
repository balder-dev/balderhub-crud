from balderhub.data.lib.scenario_features.abstract_data_item_related_feature import AbstractDataItemRelatedFeature
from balderhub.data.lib.utils.response_message_list import ResponseMessageList


class BasicInteractorFeature(AbstractDataItemRelatedFeature):
    """
    Feature class that interacts with the system-under-test in some kind.
    """

    def get_active_success_messages(self) -> ResponseMessageList:
        """
        :return: returns a list of all active success messages
        """
        # TODO do we need an observer that listens to all kind of messages during interaction
        raise NotImplementedError()

    def get_active_error_messages(self) -> ResponseMessageList:
        """
        :return: returns a list of all active error messages
        """
        # TODO do we need an observer that listens to all kind of messages during interaction
        raise NotImplementedError()
