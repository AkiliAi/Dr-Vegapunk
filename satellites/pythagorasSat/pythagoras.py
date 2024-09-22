from satellites.base_satellite import VegapunkSatellite
from typing import Dict, Any, List
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import io
import base64
import random
from utils.logger import get_logger
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import logging

load_dotenv()


# client = OpenAI(os.getenv("LLM_API_KEY"))
#
# client =OpenAI(
#     organization="LLM_API_KEY",
# )
#

role = "mathématiques, statistiques et analyse de données"
fonction = "Effectuer des calculs complexes et analyser des ensembles de données"

class Pythagoras(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Pythagoras", specialty="Role")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.llm_api_url = "https://api.openai.com/v1/chat/completions"  # Example using OpenAI's API
        self.research_databases = {
            "scientific": "https://api.example-scientific-db.com/search",
            "news": "https://api.example-news-db.com/search",
            "general": "https://api.example-general-db.com/search"
        }
        self.mathematical_constants = {
            "pi": np.pi,
            "e": np.e,
            "golden_ratio": (1 + np.sqrt(5)) / 2
        }
        self.resources = {}
        self.external_apis = {}
        self.logger = get_logger("pythagoras")

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get('type')
        if task_type == "calculate":
            return self._perform_calculation(task.get('operation'), task.get('values'))
        elif task_type == "analyze_data":
            return self._analyze_dataset(task.get('data'))
        elif task_type == "statistical_test":
            return self._perform_statistical_test(task.get('test_type'), task.get('data'))
        if task_type == "analyze_data":
            result = self.analyze_data_2(task["data"])
        elif task_type == "conduct_research":
            result = self.conduct_research(task["topic"], task.get("depth", "medium"))
        elif task_type == "extract_information":
            result = self.extract_information(task["content"], task.get("keywords", []))
        else:
            result = f"Tâche non reconnue : {task_type}"

        self.log_activity(f"Tâche traitée : {task_type}, Résultat : {result}")
        return {"result": result}

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

    def analyze_data_2(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        df = pd.DataFrame(data)
        analysis = {
            "summary": df.describe().to_dict(),
            "correlations": df.corr().to_dict(),
            "trends": self._detect_trends(df),
            "outliers": self._detect_outliers(df)
        }
        return analysis

    def conduct_research(self, topic: str, depth: str = "medium") -> Dict[str, Any]:
        research_results = {}
        for db_name, db_url in self.research_databases.items():
            research_results[db_name] = self._search_database(db_url, topic, depth)

        summary = self._summarize_research(topic, research_results)
        return {
            "topic": topic,
            "depth": depth,
            "results": research_results,
            "summary": summary
        }

    def extract_information(self, content: str, keywords: List[str] = []) -> Dict[str, Any]:
        prompt = f"Extraire les informations clés du texte suivant, en se concentrant sur les mots-clés {keywords} si fournis : {content}"
        extracted_info = self._query_llm(prompt)

        return {
            "original_content_length": len(content),
            "extracted_information": extracted_info,
            "keywords_used": keywords
        }

    def _detect_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        trends = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            trend = stats.linregress(range(len(df)), df[column])
            trends[column] = {
                "slope": trend.slope,
                "intercept": trend.intercept,
                "r_value": trend.rvalue,
                "p_value": trend.pvalue,
                "trend": "increasing" if trend.slope > 0 else "decreasing"
            }
        return trends

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, List[Any]]:
        outliers = {}
        for column in df.select_dtypes(include=[np.number]).columns:
            z_scores = np.abs(stats.zscore(df[column]))
            outliers[column] = df[column][z_scores > 3].tolist()
        return outliers

    def _search_database(self, db_url: str, topic: str, depth: str) -> List[Dict[str, Any]]:
        # Simuler une recherche dans une base de données externe
        # Dans une implémentation réelle, cela ferait un appel API à la base de données
        return [
            {"title": f"Résultat 1 pour {topic}", "summary": f"Résumé du résultat 1 pour {topic}"},
            {"title": f"Résultat 2 pour {topic}", "summary": f"Résumé du résultat 2 pour {topic}"}
        ]

    def _summarize_research(self, topic: str, research_results: Dict[str, List[Dict[str, Any]]]) -> str:
        # Utiliser le LLM pour résumer les résultats de recherche
        research_summary = json.dumps(research_results)
        prompt = f"Résumez les résultats de recherche suivants sur le sujet '{topic}' : {research_summary}"
        return self._query_llm(prompt)

    def _query_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            response = requests.post(self.llm_api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.RequestException as e:
            return f"Erreur lors de la requête LLM : {str(e)}"

    def log_activity(self, activity: str):
        logging.info(activity)

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


    def process_communication(self,sender_name:str,message:Dict[str,Any]) ->Dict[str,Any]:
        if message.get("type")== "task":
            task_result = self.process_task(message.get("task"))
            return {"status": "Traitement effectué", "result": task_result}
        elif message.get("type") == "research":
            research_result = self.conduct_research(message.get("topic"), message.get("depth"))
            return {"status": "Recherche effectuée", "result": research_result}
        elif message.get("type") == "information_extraction":
            info_result = self.extract_information(message.get("content"), message.get("keywords", []))
            return {"status": "Extraction d'information effectuée", "result": info_result}
        elif message.get("type") == "update_constants":
            self.mathematical_constants.update(message.get("constants", {}))
            return {"status": "Constantes mises à jour", "result": self.mathematical_constants}
        elif message.get("type") == "update_resources":
            self.resources.update(message.get("resources", {}))
            return {"status": "Ressources mises à jour", "result": self.resources}
        elif message.get("type") == "update_external_apis":
            self.external_apis.update(message.get("apis", {}))
            return {"status": "APIs mises à jour", "result": self.external_apis}

        else:
            return {"status": "Erreur", "result": "Type de tâche inconnu"}

    def receive_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"{self.name} received communication from {sender_name}")
        return self.process_communication(sender_name, message)

