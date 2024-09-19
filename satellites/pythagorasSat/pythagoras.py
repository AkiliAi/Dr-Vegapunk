from satellites.base_satellite import VegapunkSatellite
from typing import Dict, Any, List
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import io
import base64
import random
import logging



role = "mathématiques, statistiques et analyse de données"
fonction = "Effectuer des calculs complexes et analyser des ensembles de données"

class Pythagoras(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Pythagoras", specialty="Role")
        self.mathematical_constants = {
            "pi": np.pi,
            "e": np.e,
            "golden_ratio": (1 + np.sqrt(5)) / 2
        }
        self.resources = {}
        self.external_apis = {}

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get('type')
        if task_type == "calculate":
            return self._perform_calculation(task.get('operation'), task.get('values'))
        elif task_type == "analyze_data":
            return self._analyze_dataset(task.get('data'))
        elif task_type == "statistical_test":
            return self._perform_statistical_test(task.get('test_type'), task.get('data'))
        else:
            return {"error": "Tâche non reconnue"}

    def _perform_calculation(self, operation: str, values: List[float]) -> Dict[str, Any]:
        if not operation or not values:
            return {"error": "Opération ou valeurs manquantes"}

        try:
            if operation == "mean":
                result = np.mean(values)
            elif operation == "median":
                result = np.median(values)
            elif operation == "std_dev":
                result = np.std(values)
            elif operation == "correlation":
                if len(values) != 2 or not all(isinstance(v, list) for v in values):
                    return {"error": "La corrélation nécessite deux listes de valeurs"}
                result = np.corrcoef(values[0], values[1])[0, 1]
            else:
                return {"error": "Opération non reconnue"}

            return {"operation": operation, "result": result}
        except Exception as e:
            return {"error": f"Erreur lors du calcul: {str(e)}"}

    def _analyze_dataset(self, data: List[float]) -> Dict[str, Any]:
        if not data:
            return {"error": "Ensemble de données vide"}

        try:
            analysis = {
                "mean": np.mean(data),
                "median": np.median(data),
                "std_dev": np.std(data),
                "min": np.min(data),
                "max": np.max(data),
                "quartiles": np.percentile(data, [25, 50, 75]).tolist()
            }

            # Création d'un histogramme
            plt.figure(figsize=(10, 6))
            plt.hist(data, bins='auto', alpha=0.7, color='skyblue', edgecolor='black')
            plt.title("Histogramme des données")
            plt.xlabel("Valeurs")
            plt.ylabel("Fréquence")

            # Convertir le graphique en image base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()

            analysis["histogram"] = image_base64

            return analysis
        except Exception as e:
            return {"error": f"Erreur lors de l'analyse: {str(e)}"}

    def _perform_statistical_test(self, test_type: str, data: Dict[str, List[float]]) -> Dict[str, Any]:
        if not test_type or not data:
            return {"error": "Type de test ou données manquantes"}

        try:
            if test_type == "t_test":
                if 'group1' not in data or 'group2' not in data:
                    return {"error": "Deux groupes de données sont nécessaires pour le t-test"}
                t_stat, p_value = stats.ttest_ind(data['group1'], data['group2'])
                return {"test": "t_test", "t_statistic": t_stat, "p_value": p_value}
            elif test_type == "anova":
                if len(data) < 2:
                    return {"error": "Au moins deux groupes sont nécessaires pour l'ANOVA"}
                f_stat, p_value = stats.f_oneway(*data.values())
                return {"test": "ANOVA", "f_statistic": f_stat, "p_value": p_value}
            else:
                return {"error": "Type de test statistique non reconnu"}
        except Exception as e:
            return {"error": f"Erreur lors du test statistique: {str(e)}"}

    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        print(f"{self.name} envoie un message à Stellar: {message}")
        return {"Statut": "Message reçu", "message": "Stellar a bien reçu le message de Pythagoras"}

    def update_from_punkrecord(self):
        print(f"{self.name} met à jour sa base de connaissances depuis Punkrecord")
        new_constant = random.choice(["Constante de Planck", "Nombre d'Avogadro", "Constante de Boltzmann"])
        self.add_to_knowledge_base("Nouvelle_constante", new_constant)

    def report_status(self) -> Dict[str, Any]:
        status = super().report_status()
        status.update({
            "Constantes_mathématiques": list(self.mathematical_constants.keys()),
            "Opérations_disponibles": ["mean", "median", "std_dev", "correlation"]
        })
        return status