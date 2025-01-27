### neuer-prime

## Description 

Le joueur incarne un gardien de but en vue subjective (POV) et doit arrêter différents types de penaltys. Les mains du gardien sont contrôlées par
les mouvements réels des mains du joueur par tracking.

## Prérequis 

- cv2
- numpy
- mediapipe
- subprocess
- screeninfo
- json
- time
- requests
- API_raspberry
- math
- subprocess
- scipy

## Installation 

Après avoir cloner le projet.  
Créer un environnement virtuel :
~~~
python -m venv env
source env/bin/active
~~~
Installer les dépendances :
~~~
pip install -r requirements.txt
~~~

## Utilisation

~~~
python main.py
~~~

Le main est un menu, sur lequel il possible de choisir dans quelle section on veut aller.  
Le boutton "Jouer en Ligne" envoie sur le jeu, **il n'est possible de l'utliser que si l'on est connecté à la raspberry**.  
Le boutton "Jouer hors Ligne" envoie sur le jeu local, c'est alors une simple parti il n'y a **pas de classement à la fin**.  
Une fois sur le jeu, pour quitter l'interface, il faut appuyer sur la **touche "Echap"**.  
Le boutton "Leaderboard" envoie sur le classement des meilleurs joueurs en fonction de leur score.  
A partir du Leaderboard, **ce menu est seulement disponible si l'on est connecté à la raspberry**.   
Pour quitter le menu il suffit d'appuyer sur le boutton **"Quitter" ou la touche "Echap"**.
