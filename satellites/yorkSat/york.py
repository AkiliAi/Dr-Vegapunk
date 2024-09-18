from satellites.base_satellite import VegapunkSatellite

role = (" Gerer les tache repetitive, les tache de routine,et la maintenance des systeme")

fonction = "Gerer les tache repetitive, les resource et les maintenance des systeme"


class York(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="York", specialty=role)
        self.resources = {}

    def process_task(self, task):
        pass

    def communicate_with_stellar(self, message):
        pass

    def update_from_punkrecord(self):
        pass
