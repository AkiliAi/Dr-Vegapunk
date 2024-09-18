from satellites.base_satellite import VegapunkSatellite

role = "Analyse de données, formuler des recommandation et effectuer des recherche approfondie"

fonction = "Faire des recher sur des sujetc complexe,extraire ,analyse des information de base de donner  ou web et formuler des recommandation"


class Pythagoras(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Pythagoras", specialty="Calculs mathématiques")
        self.resources = {}

    def process_task(self, task):
        pass

    def communicate_with_stellar(self, message):
        pass

    def update_from_punkrecord(self):
        pass
