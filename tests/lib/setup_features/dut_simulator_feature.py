import balder

from tests.lib.utils.dut_simulator import DutSimulator


class DutSimulatorFeature(balder.Feature):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dut_simulator = DutSimulator()