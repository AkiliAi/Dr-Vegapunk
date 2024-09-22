import openai
from dotenv import load_dotenv
import os
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

while True:
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role":"user", "content":input("Enter your message: ")}]

    )
    if chat_response.choices[0].message.content == "Goodbye":
        break
    print(chat_response.choices[0].message.content)


print("Aurevoir")



















#
# stellar = Stellar()
# atlas = Atlas()
# lilith = Lilith()
# pythagoras = Pythagoras()
# shaka = Shaka()
# edison = Edison()
# york = York()

#
# stellar.register_satellites(atlas)
# stellar.register_satellites(lilith)
# stellar.register_satellites(pythagoras)
# stellar.register_satellites(shaka)
# stellar.register_satellites(edison)
# stellar.register_satellites(york)
#
#
# # Exemple de communication
# response = stellar.route_communication("Shaka", "Atlas", {"type": "monitor_directory", "content": "Suspicious activity detected"})
# print(response)
#
# # Exemple de diffusion
# results = stellar.broadcast_message("Shaka", {"type": "ethics_update", "content": "New ethical guidelines"})
# print(results)
