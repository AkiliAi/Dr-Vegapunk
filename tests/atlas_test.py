from satellites.atlasSat.atlas import Atlas





def test_atlas():

    atlas = Atlas()

    # Ajout de tâches à la file d'attente
    atlas.add_task({"type": "monitor_directory", "directory": "/home/user/documents"})
    atlas.add_task({"type": "check_changes"})
    atlas.add_task({"type": "send_email", "to": "user@example.com", "subject": "Alerte", "body": "Changements détectés"})
    atlas.add_task({"type": "manage_file", "action": "create", "file_path": "/tmp/test.txt"})
    atlas.add_task({"type": "execute_command", "command": "ls -l /tmp"})

    # Traitement des tâches
    while task := atlas.get_next_task():
        result = atlas.process_task(task)
        print(f"Résultat de la tâche : {result}")

    # Affichage du statut
    print(atlas.report_status())

    # Communication avec Stellar
    stellar_response = atlas.communicate_with_stellar({"message": "Rapport de sécurité quotidien"})
    print(f"Réponse de Stellar : {stellar_response}")

    # Mise à jour depuis PunkRecord
    atlas.update_from_punkrecord()


test_atlas()

