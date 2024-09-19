from satellites.base_satellite import VegapunkSatellite
from typing import Dict, Any, List
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import logging

role = "logique, éthique et analyse"
fonction = "Vérifier la cohérence des informations et filtrer les informations non éthiques"

class Shaka(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Shaka", specialty=role)
        self.nlp = self._initialize_nlp_tools()
        logging.basicConfig(filename='shaka.log', level=logging.INFO)

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
        else:
            return {"error": "Tâche non reconnue"}

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

    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        print(f"{self.name} envoie un message à Stellar: {message}")
        return {"Statut": "Message reçu", "message": "Stellar a bien reçu le message"}

    def update_from_punkrecord(self):
        print(f"{self.name} met à jour sa base de connaissances depuis Punkrecord")
        self.add_to_knowledge_base("Last_update", "Nouveaux patterns détectés dans les données")

    def perform_advanced_analyse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        text_analyse = self._analyse_text(data.get('text', ''))
        logical_analyse = self._logical_reasoning(data.get('hypothese', []), data.get('question', ''))
        print(f"{self.name} effectue une analyse avancée des données")
        return {
            "Analyse_de_texte": text_analyse,
            "Analyse_logique": logical_analyse,
            "Conclusions": "Analyse intégrale basée sur le texte et les raisonnements logiques"
        }
