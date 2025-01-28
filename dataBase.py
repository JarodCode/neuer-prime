import API_Raspberry as API

"""
Instance for leaderboard
API.delete_all_dweets_for("score")

API.dweet_for("score", {"name": "neuer", "score": 1000})
API.dweet_for("score", {"name": "quentin", "score": 800})
API.dweet_for("score", {"name": "theo", "score": 600})
API.dweet_for("score", {"name": "marius", "score": 400})
API.dweet_for("score", {"name": "tom", "score": 200})
"""

# Add a score to the leadboard, sort it it and keep only the 5 firsts

def update_leaderboard(leaderboard, name, score):

    # Add new score
    leaderboard.append((name, score))
    # Sort leaderboard descending
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    # if there is more than 6 elements in leaderboard remove the one too many
    if len(leaderboard) > 5:
        leaderboard.pop()


# Get the update leaderboard

def get_leaderboard():
    
    # Reset leaderboard
    leaderboard = [] 
    # Get scores with the API
    dico = API.get_dweets_for("score")
    scores = API.get_data(dico) 

    for name, score in scores:
        update_leaderboard(leaderboard, name, score)

    return leaderboard

# To delete all dweets :
# API.delete_all_dweets_for("score")

