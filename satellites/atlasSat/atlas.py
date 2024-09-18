from typing import Dict, Any

from satellites.base_satellite import VegapunkSatellite


class Atlas(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Atlas", specialty="Execution des tâches")

    def process_task(self, task):
        pass

    def communicate_with_stellar(self, message: Dict[str, Any]):
        pass

    def update_from_punkrecord(self):
        pass
