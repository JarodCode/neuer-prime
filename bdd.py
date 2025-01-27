import API_Raspberry as API

# Fonction pour ajouter un score et gérer le leaderboard
def update_leaderboard(leaderboard, name, score):
    leaderboard.append((name, score))  # Ajouter le nouveau score
    leaderboard.sort(key=lambda x: x[1], reverse=True)  # Trier par score décroissant
    if len(leaderboard) > 5:
        leaderboard.pop()  # Supprimer le score le plus bas si plus de 5 éléments

# Initialisation du leaderboard (vide au départ)
leaderboard = []

# Envoi des scores (tu peux garder cette partie si tu envoies les scores)
API.dweet_for("score", {"name": "theo", "score": 1})
API.dweet_for("score", {"name": "quentin", "score": 1})

# Récupération des scores depuis l'API
dico = API.get_dweets_for("score")
#print(dico)  # Affiche la liste des dweets récupérés
scores = API.get_data(dico)
#print(scores)  # Affiche les données extraites (nom et score)

# Mise à jour du leaderboard avec les scores récupérés
for name, score in scores:  # On itère directement sur les tuples (name, score)
    update_leaderboard(leaderboard, name, score)

# Afficher le leaderboard (les 5 meilleurs scores)
print("Leaderboard:", leaderboard)

# Si tu veux supprimer tous les dweets après, tu peux le faire ici
