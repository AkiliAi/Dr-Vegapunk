from satellites.edisonSat.edison import Edison


def test_edison():
    edison = Edison()

    print()


    # Test de génération d'idée
    idea_task = {"type": "generate_idea", "domain": "IA"}
    idea_result = edison.process_task(idea_task)
    print("Idée générée:", idea_result)

        # Test d'évaluation de faisabilité
    if "idea" in idea_result:
        feasibility_task = {"type": "evaluate_feasibility", "idea": idea_result["idea"]}
        feasibility_result = edison.process_task(feasibility_task)
        print("Évaluation de faisabilité:", feasibility_result)
        print()
            # Test de simulation de prototype
        prototype_task = {"type": "simulate_prototype", "idea": idea_result["idea"]}
        prototype_result = edison.process_task(prototype_task)
        print("Simulation de prototype:", prototype_result)
    print()
        # Test de communication avec Stellar
    stellar_response = edison.communicate_with_stellar({"status_update": "Nouvelle idée générée et évaluée"})
    print("Réponse de Stellar:", stellar_response)

        # Test de mise à jour depuis PunkRecord
    edison.update_from_punkrecord()

    print()

        # Affichage du statut final
    print("Statut d'Edison:", edison.report_status())


test_edison()
