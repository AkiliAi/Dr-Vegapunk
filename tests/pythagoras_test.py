from satellites.pythagorasSat.pythagoras import Pythagoras
import numpy as np


def test_pythagoras():
    pythagoras = Pythagoras()

    test_task = {
        "type": "calculate",
        "operation": "mean",
        "values": [1, 2, 3, 4, 5]
    }

    test_result = pythagoras.process_task(test_task)
    print("Résultat de la tâche de test:", test_result)
    print("\n\n")
    # Test de calcul
    calc_task = {"type": "calculate", "operation": "mean", "values": [1, 2, 3, 4, 5]}
    calc_result = pythagoras.process_task(calc_task)
    print("Résultat du calcul:", calc_result)
    print("\n\n")

    test_data = {
        "type": "analyze_data",
        "data": [1, 2, 3, 4, 5]
    }

    data_result = pythagoras.process_task(test_data)
    print("Résultat de l'analyse de données:", data_result)
    print("\n\n")
    # Test d'analyse de données
    data_task = {"type": "analyze_data", "data": np.random.normal(0, 1, 1000).tolist()}
    data_result = pythagoras.process_task(data_task)
    print("Résultat de l'analyse de données:", {k: v for k, v in data_result.items() if k != 'histogram'})
    print("Un histogramme a été généré (non affiché ici)")
    print("\n\n")

    test_test = {
        "type": "statistical_test",
        "test_type": "correlation",
        "data": [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]]
    }

    test_result = pythagoras.process_task(test_test)
    print("Résultat du test statistique:", test_result)
    print("\n\n")

    # Test de test statistique
    stat_task = {
        "type": "statistical_test",
        "test_type": "t_test",
        "data": {
            "group1": np.random.normal(0, 1, 100).tolist(),
            "group2": np.random.normal(0.5, 1, 100).tolist()
        }
    }
    stat_result = pythagoras.process_task(stat_task)
    print("Résultat du test statistique:", stat_result)
    print("\n\n")
    # Exemple de données pour l'analyse
    sample_data = [
        {"x": 1, "y": 2, "z": 3},
        {"x": 2, "y": 4, "z": 6},
        {"x": 3, "y": 6, "z": 9},
        {"x": 4, "y": 8, "z": 12},
        {"x": 5, "y": 10, "z": 15}
    ]

    # Ajout de tâches à la file d'attente
    pythagoras.add_task({"type": "analyze_data", "data": sample_data})
    pythagoras.add_task({"type": "conduct_research", "topic": "Intelligence Artificielle", "depth": "deep"})
    pythagoras.add_task({"type": "extract_information",
                         "content": "L'intelligence artificielle (IA) est un domaine de l'informatique qui vise à créer des machines capables de simuler l'intelligence humaine. Elle englobe des sous-domaines tels que l'apprentissage automatique, le traitement du langage naturel et la vision par ordinateur.",
                         "keywords": ["apprentissage automatique", "traitement du langage naturel"]})

    # Traitement des tâches
    while task := pythagoras.get_next_task():
        result = pythagoras.process_task(task)
        print(f"Résultat de la tâche : {result}")

    print("\n\n")

    print("Connexion au Punkrecord")
    pythagoras.update_from_punkrecord()

    print("Communication avec Stellar")
    stellar_response = pythagoras.communicate_with_stellar({"status_update": "Tâche terminée avec succès"})
    print("Réponse de Stellar:", stellar_response)

    print(pythagoras.report_status())


test_pythagoras()

print("test pythagoras")
print("By YmC")