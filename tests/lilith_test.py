from satellites.lilithSat.lilith import Lilith


lilith = Lilith()

# Ajout de tâches à la file d'attente
lilith.add_task({"type": "generate_idea", "domain": "Technologie"})
lilith.add_task({"type": "solve_problem", "problem": "Surpopulation urbaine"})
lilith.add_task({"type": "brainstorm", "topic": "Énergie renouvelable", "duration": 3})
lilith.add_task({"type": "challenge_assumption", "assumption": "La croissance économique est toujours bénéfique"})

# Traitement des tâches
while task := lilith.get_next_task():
    result = lilith.process_task(task)
    print(f"Résultat de la tâche : {result}")

# Affichage du statut
print(lilith.report_status())

# Communication avec Stellar
stellar_response = lilith.communicate_with_stellar(
    {"message": "Nouvelle idée disruptive générée pour le domaine de l'IA"})
print(f"Réponse de Stellar : {stellar_response}")

# Mise à jour depuis PunkRecord
lilith.update_from_punkrecord()