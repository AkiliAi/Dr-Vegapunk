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

    print("Connexion au Punkrecord")
    shaka.update_from_punkrecord()

    print("Communication avec Stellar")
    stellar_response = shaka.communicate_with_stellar({"status_update": "Tâche terminée avec succès"})
    print("Réponse de Stellar:", stellar_response)

    print(shaka.report_status())


test_shaka()
