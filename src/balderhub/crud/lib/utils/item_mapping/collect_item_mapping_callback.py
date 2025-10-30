from typing import Any

import balder
from .base_itemmapping_callback import BaseItemMappingCallback, CallbackElementObjectT


class CollectItemmappingCallback(BaseItemMappingCallback):

    def execute(self, feature: balder.Feature, field: str, element_object: CallbackElementObjectT, already_collected_data: Any) -> Any:
        pass
