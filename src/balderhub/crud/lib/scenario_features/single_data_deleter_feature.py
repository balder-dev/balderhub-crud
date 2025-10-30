from __future__ import annotations
from balderhub.crud.lib.scenario_features.basic_interactor_feature import BasicInteractorFeature


class SingleDataDeleterFeature(BasicInteractorFeature):

    def load(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError()
