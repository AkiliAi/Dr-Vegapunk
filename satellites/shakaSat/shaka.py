from satellites.base_satellite import VegapunkSatellite
from typing import Dict, Any, List, Optional
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from utils.logger import get_logger
import requests
import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



role = "logique, éthique et analyse"
fonction = "Vérifier la cohérence des informations et filtrer les informations non éthiques"

class Shaka(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Shaka", specialty=role)
        self.nlp = self._initialize_nlp_tools()
        # logging.basicConfig(filename='shaka.log', level=logging.INFO)
        self.llm_api_key = os.getenv("MISTRAL_API_KEY")
        self.llm_api_url = "https://api.mistral.ai/v1/chat/completions"  # Example using OpenAI's API
        self.fact_check_api = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        self.fact_check_api_key = os.getenv("FACT_CHECK_API_KEY")
        self.ethical_filter_active = True
        self.ethical_guidelines = [
            "Ne pas promouvoir la violence ou des activités illégales",
            "Éviter les discriminations basées sur la race, le genre, la religion, etc.",
            "Respecter la vie privée et les données personnelles",
            "Promouvoir l'honnêteté et la transparence",
            "Éviter la désinformation et les fake news"]
        self.logger = get_logger("shaka")

    def _initialize_nlp_tools(self):
        resources = ["stopwords", "punctuation", "averaged_perceptron_tagger", "wordnet", "punkt_tab"]
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                print(f"Téléchargement de la ressource {resource} pour NLTK")
                nltk.download(resource, quiet=True)

        return {
            "tokenizer": word_tokenize,
            "stopwords": set(stopwords.words('french')),
            "punctuation": set(string.punctuation)
        }

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get('type')
        if task_type == "analyse_text":
            return self._analyse_text(task['content'])
        elif task_type == 'raisonnement_logique':
            return self._logical_reasoning(task['hypothese'], task['question'])
        elif task_type == "ethical_check":
            result = self.check_ethics(task["content"])
        elif task_type == "fact_check":
            result = self.verify_facts(task["claim"])
        elif task_type == "provide_recommendations":
            result = self.provide_ethical_recommendations(task["content"])
        elif task_type == "toggle_ethical_filter":
            result = self.toggle_ethical_filter()
        else:
            result = f"Tâche non reconnue : {task_type}"

        self.log_activity(f"Tâche traitée : {task_type}, Résultat : {result}")
        return {"result": result}

    def _analyse_text(self, texte: str) -> Dict[str, Any]:
        try:
            tokens = self.nlp['tokenizer'](texte.lower())
            words = [word for word in tokens if word not in self.nlp['stopwords'] and word not in self.nlp['punctuation']]
            word_freq = nltk.FreqDist(words)
            return {
                "Nombre_de_mots": len(words),
                "Mots_uniques": len(set(words)),
                "Mots_les_plus_communs": word_freq.most_common(5)
            }
        except Exception as e:
            print(f"Erreur lors de l'analyse du texte : {e}")
            return {"error": str(e)}

    def _logical_reasoning(self, hypothese: List[str], question: str) -> Dict[str, Any]:
        combined_hypothesis = " ".join(hypothese).lower()
        question = question.lower()
        relevant_words = set(combined_hypothesis.split()) & set(question.split())
        relevance_score = len(relevant_words) / len(set(question.split()))

        return {
            "Score_de_pertinence": relevance_score,
            "Mots_pertinents": list(relevant_words),
            "Conclusion": "Basé sur le score de pertinence, les hypothèses semblent " +
                          ("pertinentes" if relevance_score > 0.5 else "peu pertinentes") + " à la question."
        }

    def check_ethics(self, content: str) -> Dict[str, Any]:
        if not self.ethical_filter_active:
            return {"status": "Le filtre éthique est désactivé", "content": content}

        prompt = f"Analysez le contenu suivant et déterminez s'il est éthique selon ces directives : {self.ethical_guidelines}. Contenu : '{content}'"
        response = self._query_llm(prompt)
        is_ethical = "éthique" in response.lower() and "non éthique" not in response.lower()

        return {
            "content": content,
            "is_ethical": is_ethical,
            "analysis": response
        }

    def verify_facts(self, claim: str) -> Dict[str, Any]:
        # Utilisation de l'API Google Fact Check Tools (nécessite une clé API valide)
        params = {
            "key": self.fact_check_api_key,
            "query": claim
        }
        try:
            response = requests.get(self.fact_check_api, params=params)
            response.raise_for_status()
            fact_checks = response.json().get("claims", [])
            if fact_checks:
                return {
                    "claim": claim,
                    "fact_check_result": fact_checks[0].get("claimReview", [])[0].get("textualRating", "Inconnu"),
                    "source": fact_checks[0].get("claimReview", [])[0].get("publisher", {}).get("name", "Inconnu")
                }
            else:
                return {"claim": claim, "fact_check_result": "Aucune vérification trouvée"}
        except requests.RequestException as e:
            return {"claim": claim, "error": f"Erreur lors de la vérification des faits : {str(e)}"}

    def provide_ethical_recommendations(self, content: str) -> Dict[str, Any]:
        prompt = f"Le contenu suivant a été jugé non éthique : '{content}'. Proposez une version alternative qui respecte ces directives éthiques : {self.ethical_guidelines}"
        response = self._query_llm(prompt)
        return {
            "original_content": content,
            "ethical_recommendation": response
        }

    def toggle_ethical_filter(self) -> Dict[str, Any]:
        self.ethical_filter_active = not self.ethical_filter_active
        status = "activé" if self.ethical_filter_active else "désactivé"
        return {"message": f"Le filtre éthique est maintenant {status}"}

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


    def perform_advanced_analyse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        text_analyse = self._analyse_text(data.get('text', ''))
        logical_analyse = self._logical_reasoning(data.get('hypothese', []), data.get('question', ''))
        print(f"{self.name} effectue une analyse avancée des données")
        return {
            "Analyse_de_texte": text_analyse,
            "Analyse_logique": logical_analyse,
            "Conclusions": "Analyse intégrale basée sur le texte et les raisonnements logiques"
        }

    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        print(f"{self.name} envoie un message à Stellar: {message}")
        return {"Statut": "Message reçu", "message": "Stellar a bien reçu le message"}

    def update_from_punkrecord(self):
        print(f"{self.name} met à jour sa base de connaissances depuis Punkrecord")
        self.add_to_knowledge_base("Last_update", "Nouveaux patterns détectés dans les données")
        return {"Statut": "Mise à jour effectuée"}

    def process_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        # Logique spécifique à Shaka pour traiter les communications
        if message.get("type") == "ethics_check":
            # Effectuer une vérification éthique
            result = self.perform_ethics_check(message.get("content"))
            return {"status": "completed", "result": result}
        elif message.get("type") == "security_alert":
            # Traiter une alerte de sécurité du point de vue éthique
            analysis = self.analyze_security_alert(message.get("content"))
            return {"status": "analyzed", "ethical_analysis": analysis}
        else:
            return {"status": "unknown_message_type"}


    def receive_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"{self.name} received communication from {sender_name}")
        return self.process_communication(sender_name, message)

    def perform_ethics_check(self, content: str) -> str:
        # Implémentez ici la logique de vérification éthique
        # Ceci est un exemple simplifié
        return f"Ethical analysis of: {content}"

    def analyze_security_alert(self, alert_content: str) -> str:
        # Implémentez ici la logique d'analyse éthique des alertes de sécurité
        # Ceci est un exemple simplifié
        return f"Ethical implications of security alert: {alert_content}"



