from satellites.yorkSat.york import York




york = York()

# Ajout de tâches à la file d'attente
york.add_task({"type": "check_resources"})
york.add_task({"type": "optimize_performance"})
york.add_task({"type": "schedule_maintenance", "component": "Serveur principal", "date": "2024-09-25"})
york.add_task({"type": "perform_maintenance", "component": "Serveur principal"})

# Traitement des tâches
while task := york.get_next_task():
    result = york.process_task(task)
    print(f"Résultat de la tâche : {result}")

print("\n")
# Affichage du statut
print(york.report_status())

print("\n")
# Communication avec Stellar
stellar_response = york.communicate_with_stellar({"message": "Rapport de performance système"})
print(f"Réponse de Stellar : {stellar_response}")
print("\n")
# Mise à jour depuis PunkRecord
york.update_from_punkrecord()