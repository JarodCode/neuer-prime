### neuer-prime

## Description 

Le joueur incarne un gardien de but en vue subjective (POV) et doit arrêter des
tirs de penalty effectués par des stars du football. Les mains du gardien sont contrôlées par
les mouvements réels du joueur par tracking.

## Prérequis 

- cv2
- numpy
- mediapipe
- subprocess

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
Le boutton "Jouer" envoie sur le jeu,  
Une fois sur le jeu, pour quitter l'interface, il faut appuyer sur la **touche "q"**.  
Le boutton "Leaderboard" envoie sur le classement des meilleurs joueurs en fonction de leur score.  
A partir du Leaderboard, il y a un boutton "Statistiques"  
qui envoie sur un menu où des statistiques seront affichées (ex hitmap).  
Pour quitter le menu il suffit d'appuyer sur le boutton "Quitter" ou la touche "Echap".
