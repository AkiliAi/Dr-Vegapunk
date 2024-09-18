from satellites.base_satellite import VegapunkSatellite

role = " Explorer des solution non conventionnel , creatove,voir risqué"

fonction = "Generer des idee novatrices o explorer des solution non conventionnel"


class Lilith(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Lilith", specialty=role)
        self.resources = {}

    def process_task(self, task):
        pass

    def communicate_with_stellar(self, message):
        pass

    def update_from_punkrecord(self):
        pass
