from satellites.shakaSat.shaka import  Shaka



def test_shaka():
    shaka = Shaka()

    test_task = {
        "type": "analyse_text",
        "content": "L'intelligence artificielle est en train de révolutionner la manière dont nous approchons et résolvons les problèmes"
    }

    test_result = shaka.process_task(test_task)
    print("Résultat de la tâche de test:", test_result)

    test_logic = {
        "type": "raisonnement_logique",
        "hypothese": ["Tous les hommes sont mortels", "Socrate est un homme"],
        "question": "Socrate est-il mortel?"
    }

    logic_result = shaka.process_task(test_logic)
    print("Résultat de la tâche de logique:", logic_result)
    # Ajout de tâches à la file d'attente
    shaka.add_task({"type": "ethical_check",
                    "content": "Les gens devraient toujours dire la vérité, même si cela peut blesser quelqu'un."})
    shaka.add_task({"type": "fact_check", "claim": "La Terre est plate."})
    shaka.add_task({"type": "provide_recommendations", "content": "Tous les immigrants devraient être expulsés."})
    shaka.add_task({"type": "toggle_ethical_filter"})

    # Traitement des tâches
    while task := shaka.get_next_task():
        result = shaka.process_task(task)
        print(f"Résultat de la tâche : {result}")

    print("Connexion au Punkrecord")
    shaka.update_from_punkrecord()

    print("Communication avec Stellar")
    stellar_response = shaka.communicate_with_stellar({"status_update": "Tâche terminée avec succès"})
    print("Réponse de Stellar:", stellar_response)

    print(shaka.report_status())


test_shaka()
