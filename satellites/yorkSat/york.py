import psutil
import time
from typing import Dict, Any, List
from satellites.base_satellite import VegapunkSatellite
from utils.logger import get_logger
import logging

role = "Gestion des ressources et maintenance système"

fonction = "Gerer les tache repetitive, les resource et les maintenance des systeme"


class York(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="York", specialty=role)
        self.resource_thresholds ={
            "cpu": 90,
            "memory": 90,
            "disk": 90,
            "network": 75,
        }
        self.maintenance_schedule = {}
        # logging.basicConfig(filename='york.log', level=logging.INFO)
        self.external_apis = {}
        from utils.logger import get_logger

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        if task_type == "check_resources":
            result = self.check_system_resources()
        elif task_type == "optimize_performance":
            result = self.optimize_system_performance()
        elif task_type == "schedule_maintenance":
            result = self.schedule_maintenance(task["component"], task["date"])
        elif task_type == "perform_maintenance":
            result = self.perform_maintenance(task["component"])
        else:
            result = f"Tâche non reconnue : {task_type}"

        self.log_activity(f"Tâche traitée : {task_type}, Résultat : {result}")
        return {"result": result}

    def check_system_resources(self) -> Dict[str, Any]:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        status = {
            "cpu": "Normal" if cpu_usage < self.resource_thresholds["cpu"] else "Élevé",
            "memory": "Normal" if memory_usage < self.resource_thresholds["memory"] else "Élevé",
            "disk": "Normal" if disk_usage < self.resource_thresholds["disk"] else "Élevé",
            "network": "Normal"  # Simplified for this example
        }

        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "network_usage": network_usage,
            "status": status
        }

    def optimize_system_performance(self) -> Dict[str, Any]:
        # Simulation d'optimisation du système
        optimizations = []
        if psutil.cpu_percent() > self.resource_thresholds["cpu"]:
            optimizations.append("Réduction de la charge CPU")
        if psutil.virtual_memory().percent > self.resource_thresholds["memory"]:
            optimizations.append("Libération de mémoire")
        if psutil.disk_usage('/').percent > self.resource_thresholds["disk"]:
            optimizations.append("Nettoyage de l'espace disque")

        return {
            "optimizations_performed": optimizations,
            "performance_improvement": f"{len(optimizations) * 5}%"  # Simulated improvement
        }

    def schedule_maintenance(self, component: str, date: str) -> Dict[str, Any]:
        self.maintenance_schedule[component] = date
        return {
            "component": component,
            "scheduled_date": date,
            "status": "Maintenance programmée"
        }

    def perform_maintenance(self, component: str) -> Dict[str, Any]:
        if component in self.maintenance_schedule:
            # Simulation de maintenance
            time.sleep(2)  # Simule le temps de maintenance
            del self.maintenance_schedule[component]
            return {
                "component": component,
                "status": "Maintenance effectuée",
                "result": "Performances du composant améliorées"
            }
        else:
            return {
                "component": component,
                "status": "Erreur",
                "result": "Aucune maintenance programmée pour ce composant"
            }

    def log_activity(self, activity: str):
        logging.info(activity)

    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        self.log_activity(f"Communication avec Stellar : {message}")
        return {"status": "Message reçu par Stellar", "details": message}

    def update_from_punkrecord(self) -> None:
        self.log_activity("Mise à jour depuis PunkRecord")
        # Ici, vous pourriez implémenter la logique pour mettre à jour les seuils de ressources ou les plannings de maintenance

    def process_communication(self,sender_name:str,message:Dict[str,Any]) ->Dict[str,Any]:
        if message.get("type") == "task":
            task_result = self.process_task(message.get("task"))
            return {"status": "Traitement effectué", "result": task_result}
        elif message.get("type") == "resource_thresholds":
            self.resource_thresholds = message.get("thresholds")
            return {"status": "Seuils de ressources mis à jour", "result": self.resource_thresholds}
        elif message.get("type") == "maintenance_schedule":
            self.maintenance_schedule = message.get("schedule")
            return {"status": "Planning de maintenance mis à jour", "result": self.maintenance_schedule}
        elif message.get("type") == "external_api":
            api_name = message.get("api_name")
            api_config = message.get("api_config")
            self.external_apis[api_name] = api_config
            return {"status": "API externe ajoutée", "result": api_config}
        else:
            return {"status": "Message non reconnu", "result": "Aucune action effectuée"}



    def receive_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"{self.name} received communication from {sender_name}")
        return self.process_communication(sender_name, message)

