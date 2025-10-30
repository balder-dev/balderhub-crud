from typing import Any

import balder
from .base_itemmapping_callback import BaseItemMappingCallback, CallbackElementObjectT


class FillItemmappingCallback(BaseItemMappingCallback):

    def execute(self, feature: balder.Feature, field: str, element_object: CallbackElementObjectT, data_to_fill: Any) -> Any:
        pass
