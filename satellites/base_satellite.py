from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from abc import ABC, abstractmethod
from typing import List,Dict,Any


class  BaseSatellite(ABC):
    def __init__(self,name:str,specialty:str):
        self.name = name
        self.specialty = specialty
        self.knowledge_base = {}
        self.task_queue = []


    @abstractmethod
    def process_task(self,task:Dict[str,Any]) -> Dict[str,Any]:
        """
        Traite une tache specifique au satellite
        a implementer dans chaque classe de satellite specifique
        """
        pass
    def add_to_knowledge_base(self,key:str,value:Any):
        # Ajoute une information a la base de connaissance du satellite
        self.knowledge_base[key] = value
    def get_from_knowledge_base(self,key:str) -> Any:
        # Recupere une information de la base de connaissance du satellite
        return self.knowledge_base.get(key)

    def add_task(self,task:Dict[str,Any]):
        # Ajoute une tache a la file d'attente du satellite
        self.task_queue.append(task)

    def get_next_task(self) -> Dict[str,Any]:
        # Recupere la prochaine tache a traiter
        if self.task_queue:
            return self.task_queue.pop(0)
        return None

    def report_status(self):
        # Rapporte le status du satellite
        return {
            "name":self.name,
            "specialty":self.specialty,
            "knowledge_base":self.knowledge_base,
            "task_queue":self.task_queue,
            "task_pending":len(self.task_queue),
            "Knowledge_base_size": len(self.knowledge_base),
        }

    @abstractmethod
    def communicate_with_stellar(self,message:Dict[str,Any]) -> Dict[str,Any]:
        """
         Méthode pour communiquer avec le satellite manager (Stellar).
        À implémenter dans chaque classe de satellite spécifique.
        """
        pass

    def update_from_punkrocord(self) -> None:
        # Methode pour mettre a jour de la base de connaissance local du satellite depuis punkrecord
        pass













#
#
# class Satellite:
#     def __init__(self, name, specialty):
#         self.name = name
#         self.specialty = specialty
#         self.llm = OpenAI(temperature=0.7)
#         self.memory = ConversationBufferMemory(memory_key="chat_history")
#         self.prompt = PromptTemplate(
#             input_variables=["chat_history", "human_input", "specialty"],
#             template="""You are {specialty}.
#             Chat History: {chat_history}
#             Human: {human_input}
#             AI Assistant:"""
#         )
#         self.chain = LLMChain(
#             llm=self.llm,
#             prompt=self.prompt,
#             memory=self.memory,
#         )
#
#     def process(self, input_text):
#         return self.chain.run(human_input=input_text, specialty=self.specialty)
#
#
# # Exemple d'utilisation
# shaka = Satellite("Shaka", "an AI specializing in wisdom and general knowledge")
# response = shaka.process("Tell me about the importance of knowledge.")
# print(response)