from satellites.edisonSat.edison import Edison


def test_edison():
    edison = Edison()

    # Ajout de tâches à la file d'attente
    edison.add_task({"type": "solve_logic_problem",
                     "problem": "Si A implique B, et B implique C, que peut-on dire de la relation entre A et C?"})
    edison.add_task({"type": "perform_complex_calculation", "expression": "derivative(x^2 + 2x + 1, x)"})
    edison.add_task({"type": "generate_innovation", "domain": "énergie renouvelable"})
    edison.add_task({"type": "analyze_data",
                     "data": [{"type": "numeric", "value": 10}, {"type": "numeric", "value": 20},
                              {"type": "numeric", "value": 30}]})

    # Traitement des tâches
    while task := edison.get_next_task():
        result = edison.process_task(task)
        print(f"Résultat de la tâche : {result}")

    # Affichage du statut
    print(edison.report_status())

    # Communication avec Stellar
    stellar_response = edison.communicate_with_stellar(
        {"message": "Nouvelle innovation générée dans le domaine de l'énergie renouvelable"})
    print(f"Réponse de Stellar : {stellar_response}")

    # Mise à jour depuis PunkRecord
    edison.update_from_punkrecord()


test_edison()
