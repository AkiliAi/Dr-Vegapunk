from abc import ABC, abstractmethod
from typing import Dict, Any, Optional , List
from langchain.graphs import StateGraph, Node
import logging


class VegapunkSystem():
    def __init__(self):
        # self.satellites = {}
        self.graph = StateGraph()

        self.shaka_node = Node(self.shaka_process)
        self.atlas_node = Node(self.atlas_process)
        self.edison_node = Node(self.edison_process)
        self.lilith_node = Node(self.lilith_process)
        self.pythagoras_node = Node(self.pythagoras_process)
        self.york_node = Node(self.york_process)

        self.graph.add_node(self.shaka_node)
        self.graph.add_node(self.atlas_node)
        self.graph.add_node(self.edison_node)
        self.graph.add_node(self.lilith_node)
        self.graph.add_node(self.pythagoras_node)
        self.graph.add_node(self.york_node)

    #     definir les transitions entre les noeuds
    #     self.graph.add_edge(self.shaka_node, self.atlas_node)
    #     self.graph.add_edge(self.atlas_node, self.edison_node)
    #     self.graph.add_edge(self.edison_node, self.lilith_node)
    def shaka_process(self, input_data):
        pass

    def atlas_process(self, input_data):
        pass

    def edison_process(self, input_data):
        pass

    def lilith_process(self, input_data):
        pass

    def pythagoras_process(self, input_data):
        pass

    def york_process(self, input_data):
        pass

    def proccess_request(self, initial_input):
        return self.graph.run(initial_input)


class VegapunkSatellite(ABC):
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.knowledge_base = {}
        self.task_queue = []

    @abstractmethod
    def think(self,task: Dict[str, Any]) -> List[str]:
        pass

    @abstractmethod
    def act(self, thought: str) -> Dict[str, Any]:
        """Exécuter une action basée sur une pensée."""
        pass

    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        thoughts = self.think(task)
        results = []
        for pensee in thoughts:
            results = self.act(pensee)
            results.append(results)

        return self.systhesize_results(results)


    @abstractmethod
    def systhesize_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass



    def add_to_knowledge_base(self, key: str, value: Any):
        # Ajoute une information a la base de connaissance du satellite
        self.knowledge_base[key] = value

    def get_from_knowledge_base(self, key: str) -> Any:
        # Recupere une information de la base de connaissance du satellite
        return self.knowledge_base.get(key)

    def add_task(self, task: Dict[str, Any]):
        # Ajoute une tache a la file d'attente du satellite
        self.task_queue.append(task)

    def get_next_task(self) -> Dict[str, Any]:
        """Récupère et supprime la prochaine tâche de la file d'attente."""
        if self.task_queue:
            return self.task_queue.pop(0)
        return None

    def report_status(self):
        # Rapporte le status du satellite
        return {
            "name": self.name,
            "specialty": self.specialty,
            "knowledge_base": self.knowledge_base,
            "task_queue": self.task_queue,
            "task_pending": len(self.task_queue),
            "Knowledge_base_size": len(self.knowledge_base),
        }

    @abstractmethod
    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
         Méthode pour communiquer avec le satellite manager (Stellar).
        À implémenter dans chaque classe de satellite spécifique.
        """
        pass

    def update_from_punkrecord(self) -> None:
        # Methode pour mettre a jour de la base de connaissance local du satellite depuis punkrecord
        pass

        # Methode pour communiquer avec un autre satellite

    def communicate_with_other_satellite(self, satellite: 'VegapunkSatellite', message: Dict[str, Any]) -> Optional[
        Dict[str, Any]]:
        if not isinstance(satellite, VegapunkSatellite):
            logging.error(f"Le satellite spécifié n'est pas valide :{type(satellite)}")
            return None

        try:
            response = satellite.receive_communication(self.name, message)
            logging.info(f"Communication avec {satellite.name} : {response}")
            return response
        except Exception as e:
            logging.error(f"Erreur lors de la communication avec {satellite.name} : {str(e)}")
            return None

    def receive_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"{self.name} a recu un message de : {sender_name}")
        return self.process_communication(sender_name, message)

    @abstractmethod
    def process_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        traite le message recu d'un autre satellite
        a implementer dans chaque classe de satellite specifique
        """
        pass
