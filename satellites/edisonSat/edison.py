from satellites.base_satellite import VegapunkSatellite
from typing import Dict,Any,List
import logging
import requests
import os
from utils import logger
import json

role = "innovation et technologie"
fonction = "Générer des idées innovantes et évaluer leur faisabilité technique"


class Edison(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Edison", specialty=role)
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.llm_api_url = "https://api.openai.com/v1/chat/completions"  # Example using OpenAI's API
        self.external_apis = {
            "math": "http://api.mathjs.org/v4/",
            "wolfram": "http://api.wolframalpha.com/v1/result"
        }
        # logging.basicConfig(filename='edison_log.txt', level=logging.INFO)
        self.logger = logger.get_logger("edison")

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        if task_type == "solve_logic_problem":
            result = self.solve_logic_problem(task["problem"])
        elif task_type == "perform_complex_calculation":
            result = self.perform_complex_calculation(task["expression"])
        elif task_type == "generate_innovation":
            result = self.generate_innovation(task["domain"])
        elif task_type == "analyze_data":
            result = self.analyze_data(task["data"])
        else:
            result = f"Tâche non reconnue : {task_type}"

        self.log_activity(f"Tâche traitée : {task_type}, Résultat : {result}")
        return {"result": result}

    def solve_logic_problem(self, problem: str) -> Dict[str, Any]:
        prompt = f"Résolvez le problème logique suivant étape par étape : {problem}"
        response = self._query_llm(prompt)
        return {
            "problem": problem,
            "solution": response,
            "method": "LLM"
        }

    def perform_complex_calculation(self, expression: str) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self.external_apis['math']}?expr={expression}")
            result = response.text
        except requests.RequestException as e:
            result = f"Erreur lors du calcul : {str(e)}"

        return {
            "expression": expression,
            "result": result,
            "method": "External API (Math.js)"
        }

    def generate_innovation(self, domain: str) -> Dict[str, Any]:
        prompt = f"Générez une idée innovante dans le domaine de {domain}. Décrivez l'idée, son impact potentiel et les défis de mise en œuvre."
        response = self._query_llm(prompt)
        return {
            "domain": domain,
            "innovation": response,
            "method": "LLM"
        }

    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Pour cet exemple, nous allons simplement calculer quelques statistiques de base
        # Dans une implémentation réelle, vous pourriez utiliser des bibliothèques comme pandas ou numpy
        if not data:
            return {"error": "Aucune donnée à analyser"}

        numeric_values = [float(item['value']) for item in data if item['type'] == 'numeric']
        if numeric_values:
            analysis = {
                "count": len(numeric_values),
                "sum": sum(numeric_values),
                "average": sum(numeric_values) / len(numeric_values),
                "min": min(numeric_values),
                "max": max(numeric_values)
            }
        else:
            analysis = {"error": "Aucune donnée numérique trouvée pour l'analyse"}

        return {
            "data": data,
            "analysis": analysis,
            "method": "Internal calculation"
        }

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
        self.log_activity(f"Communication avec Stellar : {message}")
        return {"status": "Message reçu par Stellar", "details": message}

    def update_from_punkrecord(self) -> None:
        self.log_activity("Mise à jour depuis PunkRecord")
        # Ici, vous pourriez implémenter la logique pour mettre à jour les API externes ou les paramètres du modèle LLM
