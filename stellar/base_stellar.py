from satellites.base_satellite import VegapunkSatellite
from abc import ABC, abstractmethod
from typing import  Dict, Any,Optional
import logging




class Stellar:
    def __init__(self):
        self.satellites = {} # dictionnaire pour stocke les references satellites


    def register_satellites(self,satellite:VegapunkSatellite)->None:
        self.satellites[satellite.name] = satellite

    def route_communication(self, sender_name: str, target_name: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if sender_name not in self.satellites or target_name not in self.satellites:
            logging.error(f"Invalid sender or target: {sender_name} -> {target_name}")
            return None

        sender = self.satellites[sender_name]
        target = self.satellites[target_name]

        return sender.communicate_with_other_satellite(target, message)

    def broadcast_message(self, sender_name: str, message: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        results = {}
        for satellite_name, satellite in self.satellites.items():
            if satellite_name != sender_name:
                results[satellite_name] = self.route_communication(sender_name, satellite_name, message)
        return results
