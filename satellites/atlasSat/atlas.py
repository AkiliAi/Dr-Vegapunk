import os
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any, List
from satellites.base_satellite import VegapunkSatellite
import logging
import subprocess
import time
from utils.logger import get_logger


role = "Sécurité et Automatisation"
fonction = "Exécuter des tâches spécifiques ,Sécurité et Automatisation"
class Atlas(VegapunkSatellite):
    def __init__(self):
        super().__init__(name="Atlas", specialty=role)
        self.monitored_directories = []
        self.email_config ={}
        self.external_systems = {}
        # logging.basicConfig(filename='atlas.log', level=logging.INFO)
        self.llm_api_key = os.getenv("MISTRAL_API_KEY")
        self.llm_api_url = "https://api.mistral.ai/v1/chat/completions"  # Example usi
        self.logger = get_logger("atlas")
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        if task_type == "monitor_directory":
            result = self.monitor_directory(task["directory"])
        elif task_type == "check_changes":
            result = self.check_directory_changes()
        elif task_type == "send_email":
            result = self.send_email(task["to"], task["subject"], task["body"])
        elif task_type == "manage_file":
            result = self.manage_files(task["action"], task["file_path"])
        elif task_type == "execute_command":
            result = self.execute_system_command(task["command"])
        else:
            result = f"Tâche non reconnue : {task_type}"

        self.log_activity(f"Tâche traitée : {task_type}, Résultat : {result}")
        return {"result": result}


    def monitor_directory(self,directory:str) -> str:
        if os.path.exists(directory):
            self.monitored_directories.append(directory)
            return f"Répertoire {directory} ajouté à la liste de surveillance"
        else:
            return f"Répertoire {directory} inexistant"

    def check_directory_changes(self) -> List[str]:
        changes = []
        for directory in self.monitored_directories:
            try:
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.getmtime(file_path) > self.get_from_knowledge_base("last_check_time"):
                        changes.append(f"Fichier modifié : {file_path}")
            except Exception as e:
                changes.append(f"Erreur lors de la vérification de {directory}: {str(e)}")
        self.add_to_knowledge_base("last_check_time", time.time())
        return changes

    def send_email(self, to: str, subject: str, body: str) -> str:
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.email_config.get("from")
            msg["To"] = to

            server = smtplib.SMTP(self.email_config.get("smtp_server"), self.email_config.get("smtp_port"))
            server.starttls()
            server.login(self.email_config.get("username"), self.email_config.get("password"))
            server.sendmail(self.email_config.get("from"), [to], msg.as_string())
            server.quit()
            return "Email envoyé avec succès"
        except Exception as e:
            return f"Erreur lors de l'envoi de l'email : {str(e)}"

    def manage_files(self, action: str, file_path: str) -> str:
        try:
            if action == "create":
                with open(file_path, 'w') as f:
                    f.write("")
                return f"Fichier créé : {file_path}"
            elif action == "delete":
                os.remove(file_path)
                return f"Fichier supprimé : {file_path}"
            elif action == "move":
                new_path = input("Entrez le nouveau chemin : ")
                os.rename(file_path, new_path)
                return f"Fichier déplacé de {file_path} vers {new_path}"
            else:
                return "Action non reconnue. Utilisez 'create', 'delete' ou 'move'."
        except Exception as e:
            return f"Erreur lors de la gestion du fichier : {str(e)}"

    def execute_system_command(self, command: str) -> str:
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return f"Commande exécutée. Sortie : {result.stdout.decode()}"
        except subprocess.CalledProcessError as e:
            return f"Erreur lors de l'exécution de la commande : {e.stderr.decode()}"

    def log_activity(self, activity: str):
        logging.info(activity)

    def communicate_with_stellar(self, message: Dict[str, Any]) -> Dict[str, Any]:
        # Implémentation de la communication avec Stellar
        self.log_activity(f"Communication avec Stellar : {message}")
        # Ici, vous pourriez implémenter la logique réelle de communication
        return {"status": "Message reçu par Stellar", "details": message}

    def update_from_punkrecord(self) -> None:
        # Implémentation de la mise à jour depuis PunkRecord
        self.log_activity("Mise à jour depuis PunkRecord")
        # Ici, vous pourriez implémenter la logique réelle de mise à jour
        # Par exemple :
        # new_data = punkrecord.get_updates_for_atlas()
        # self.add_to_knowledge_base("email_config", new_data.get("email_config"))
        # self.add_to_knowledge_base("security_level", new_data.get("security_level"))

    def report_status(self):
        # Rapporte le status du satellite
        status = super().report_status()
        status.update({
            "Monitored_directories": self.monitored_directories,
            "Email_config": self.email_config
        })



    def process_communication(self,sender_name:str,message:Dict[str,Any]) ->Dict[str,Any]:

        if message.get("type") == "task":
            task_result = self.process_task(message.get("task"))
            return {"status": "Traitement effectué", "result": task_result}
        elif message.get("type") == "email_config":
            self.email_config = message.get("content")
            return {"status": "Configuration email mise à jour", "result": self.email_config}
        elif message.get("type") == "system_command":
            command_result = self.execute_system_command(message.get("command"))
            return {"status": "Commande système exécutée", "result": command_result}
        elif message.get("type") == "file_management":
            file_result = self.manage_files(message.get("action"), message.get("file_path"))
            return {"status": "Gestion de fichier effectuée", "result": file_result}
        elif message.get("type") == "monitor_directory":
            monitor_result = self.monitor_directory(message.get("directory"))
            return {"status": "Surveillance de répertoire effectuée", "result": monitor_result}
        elif message.get("type") == "email":
            email_result = self.send_email(message.get("to"), message.get("subject"), message.get("body"))
            return {"status": "Email envoye", "result": email_result}
        elif message.get("type") == "status_report":
            result = self.report_status()
            return {"status": "Rapport de status généré", "result": result}
        elif message.get("type") == "check_changes":
            changes = self.check_directory_changes()
            return {"status": "Changements vérifiés", "result": changes}
        else:
            return {"status": "Erreur", "result": "Type de tâche inconnu"}

    def receive_communication(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"{self.name} received communication from {sender_name}")
        return self.process_communication(sender_name, message)
