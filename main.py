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

response = Stellar.route_communication("Atlas", "York", {"type": "check_resources"})

results = Stellar.broadcast_message("Atlas", {"type": "check_resources"})


print(results)