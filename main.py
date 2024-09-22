from stellar.base_stellar import Stellar
from satellites.atlasSat.atlas import Atlas
from satellites.lilithSat.lilith import Lilith
from satellites.pythagorasSat.pythagoras import Pythagoras
from satellites.shakaSat.shaka import Shaka
from satellites.edisonSat.edison import Edison
from satellites.yorkSat.york import York
from typing import Dict, Any

stellar = Stellar()
atlas = Atlas()
lilith = Lilith()
pythagoras = Pythagoras()
shaka = Shaka()
edison = Edison()
york = York()



stellar.register_satellites(atlas)
stellar.register_satellites(lilith)
stellar.register_satellites(pythagoras)
stellar.register_satellites(shaka)
stellar.register_satellites(edison)
stellar.register_satellites(york)


# Exemple de communication
response = stellar.route_communication("Shaka", "Atlas", {"type": "monitor_directory", "content": "Suspicious activity detected"})
print(response)

# Exemple de diffusion
results = stellar.broadcast_message("Shaka", {"type": "ethics_update", "content": "New ethical guidelines"})
print(results)