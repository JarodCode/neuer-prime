import API_Raspberry as API

"""
API.delete_all_dweets_for("score")


API.dweet_for("score", {"name": "neuer", "score": 1000})
API.dweet_for("score", {"name": "quentin", "score": 800})
API.dweet_for("score", {"name": "theo", "score": 600})
API.dweet_for("score", {"name": "marius", "score": 400})
API.dweet_for("score", {"name": "tom", "score": 200})"""

# Fonction pour ajouter un score et gérer le leaderboard
def update_leaderboard(leaderboard, name, score):
    leaderboard.append((name, score))  # Ajouter le nouveau score
    leaderboard.sort(key=lambda x: x[1], reverse=True)  # Trier par score décroissant
    if len(leaderboard) > 5:
        leaderboard.pop()  # Supprimer le score le plus bas si plus de 5 éléments


# Fonction pour récupérer un leaderboard mis à jour
def get_leaderboard():
    leaderboard = []  # Réinitialiser le leaderboard
    dico = API.get_dweets_for("score")
    scores = API.get_data(dico)  # Récupérer les scores via l'API

    for name, score in scores:
        update_leaderboard(leaderboard, name, score)

    return leaderboard

# Si tu veux supprimer tous les dweets après, tu peux le faire ici
#API.delete_all_dweets_for("score")

print(get_leaderboard())
