import cv2
import numpy as np
import subprocess
import API_Raspberry as API
from Graphics import Graphic, SceneRender
from Tir import Tir
from Ballon import Ballon
from screeninfo import get_monitors
import bdd

# Couleurs
white = (255, 255, 255)   # Blanc classique pour le texte ou le fond
black = (0, 0, 0)         # Noir pour les contours ou le texte contrasté
blue = (180, 130, 70)     # Bleu acier (Steel Blue), doux et agréable
red = (60, 20, 220)       # Rouge cramoisi (Crimson), vibrant mais pas agressif
green = (50, 205, 50)     # Vert citron vert (Lime Green), vif et rafraîchissant
orange = (0, 165, 255)    # Orange vif, énergique et engageant
purple = (219, 112, 147)  # Violet moyen (Medium Purple), chic et subtil
gray = (169, 169, 169)    # Gris foncé (Dark Gray), neutre et élégant
cyan = (255, 255, 0)      # Cyan vif, pour des éléments dynamiques
yellow = (0, 215, 255)    # Jaune doré (Gold), lumineux et accrocheur

#buttons coordinates : [min x, max x, min y, max y]
#main menu
xy_jouer = [300, 500, 100, 160]
xy_leaderboard = [250, 550, 200, 260]
xy_quitter = [300, 500, 300, 360]
#leaderboard menu
xy_retour_lbd = [0, 200, 540, 600]
xy_stat_lbd = [550, 800, 540, 600]

window_width, window_height = 800, 600  # Taille de la fenêtre

#backgrounds (main menu, "statistiques" and leaderboard menus)
img_main_path = "img/fond_main.jpg"
background_main = cv2.imread(img_main_path)
background_main = cv2.resize(background_main, (window_width, window_height))

img_lbd_path = "img/fond_ldb.jpg"
background_lbd = cv2.imread(img_lbd_path)
background_lbd = cv2.resize(background_lbd, (window_width, window_height))

#main while (show menu)
showWindow = False

#initial state
state = "main_menu"

#what button have to be highlighted
buttonToHighlight = None

def update_leaderboard():
    global leaderboard
    leaderboard = bdd.get_leaderboard()  # Récupérer un leaderboard actualisé


# Fonction pour détecter les clics sur les boutons
def mouse_event(event, x, y, flags, param):
    global buttonToHighlight
    global state  # Déclare que vous utilisez la variable globale "state"
    global showWindow
    #left click
    if event == cv2.EVENT_LBUTTONDOWN:
        #if in main menu
        if state == "main_menu":
            if xy_jouer[0] <= x <= xy_jouer[1] and xy_jouer[2] <= y <= xy_jouer[3]:  # "Jouer" button
                print("Jouer !")
                subprocess.Popen(["python3", "jeu.py"])

            elif xy_leaderboard[0] <= x <= xy_leaderboard[1] and xy_leaderboard[2] <= y <= xy_leaderboard[3]: # "Leaderboard" button                
                print("Affichage du leaderboard")
                update_leaderboard()  # Actualise le leaderboard
                state = "leaderboard"
                

                            
            elif xy_quitter[0] <= x <= xy_quitter[1] and xy_quitter[2] <= y <= xy_quitter[3]:  # "Quitter" button
                print("Quitter...")
                showWindow = False
        
        #if in leaderboard 
        elif state == "leaderboard" : 
            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:     #back button
                print("Retour au menu principal")
                state = "main_menu"
            if xy_stat_lbd[0] <= x <= xy_stat_lbd[1] and xy_stat_lbd[2] <= y <= xy_stat_lbd[3]:     #"statistiques" button
                print("Affichage des statistiques")
                state = "statistiques"

        #if in "statistiques" 
        elif state == "statistiques" : 
            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:     #back button
                print("Retour au leaderboard")
                state = "leaderboard"
    
    #to follow mouse movement and to change the button to highlight
    elif event == cv2.EVENT_MOUSEMOVE:
        #if in main menu
        if state == "main_menu":
            if xy_jouer[0] <= x <= xy_jouer[1] and xy_jouer[2] <= y <= xy_jouer[3]:  # "Jouer" button
                buttonToHighlight = "Jouer"                

            elif xy_leaderboard[0] <= x <= xy_leaderboard[1] and xy_leaderboard[2] <= y <= xy_leaderboard[3]: # "Leaderboard" button
                buttonToHighlight = "Leaderboard"
            
            elif xy_quitter[0] <= x <= xy_quitter[1] and xy_quitter[2] <= y <= xy_quitter[3]:  # "Quitter" button
                buttonToHighlight = "Quitter"

            else : #no buton to highlight
                buttonToHighlight = None
        
        #if in leaderboard 
        elif state == "leaderboard" : 
            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:     #back button
                buttonToHighlight = "Retour"
            elif xy_stat_lbd[0] <= x <= xy_stat_lbd[1] and xy_stat_lbd[2] <= y <= xy_stat_lbd[3]:     #"statistiques" button
                buttonToHighlight = "Statistiques"
            else : #no buton to highlight
                buttonToHighlight = None

        #if in "statistiques" 
        elif state == "statistiques" : 
            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:     #back button
                buttonToHighlight = "Retour2"
            else : #no buton to highlight
                buttonToHighlight = None

       

# Ajouter les boutons par-dessus l'image de fond
def draw_main_menu(img):    
    
    # Dessiner le bouton "Jouer"
    cv2.rectangle(img, (xy_jouer[0], xy_jouer[2]), (xy_jouer[1], xy_jouer[3]), blue, -1)  
    cv2.putText(img, "JOUER", (350, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Jouer":
            cv2.rectangle(img, (xy_jouer[0], xy_jouer[2]), (xy_jouer[1], xy_jouer[3]), black, 2)  
    

    # Dessiner le bouton "Leaderboard"
    cv2.rectangle(img, (xy_leaderboard[0], xy_leaderboard[2]), (xy_leaderboard[1], xy_leaderboard[3]), orange, -1)  
    cv2.putText(img, "LEADERBOARD", (285, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Leaderboard":
            cv2.rectangle(img, (xy_leaderboard[0], xy_leaderboard[2]), (xy_leaderboard[1], xy_leaderboard[3]), black, 2)  


    # Dessiner le bouton "Quitter"
    cv2.rectangle(img, (xy_quitter[0], xy_quitter[2]), (xy_quitter[1], xy_quitter[3]), red, -1) 
    cv2.putText(img, "QUITTER", (332, 340), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Quitter":
        cv2.rectangle(img, (xy_quitter[0], xy_quitter[2]), (xy_quitter[1], xy_quitter[3]), black, 2) 

global leaderboard

def draw_leaderboard(img):
    
    # Afficher les scores du leaderboard
    for i, (name, score) in enumerate(leaderboard):
        text = f"{name}: {score}"  # Afficher le rang, le nom et le score
        cv2.putText(img, text, (xy_leaderboard[0] + 30, 140 + (i * 104)), cv2.FONT_HERSHEY_COMPLEX, 1, black, 2)    
    
    #draw return button
    cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), gray, -1)  
    cv2.putText(img, "RETOUR", (35, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Retour":
        cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), black, 2)  


    #draw "statistique" button
    cv2.rectangle(img, (xy_stat_lbd[0], xy_stat_lbd[2]), (xy_stat_lbd[1], xy_stat_lbd[3]), green, -1)  
    cv2.putText(img, "STATISTIQUES", (562, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Statistiques":
        cv2.rectangle(img, (xy_stat_lbd[0], xy_stat_lbd[2]), (xy_stat_lbd[1], xy_stat_lbd[3]), black, 2)  


def draw_stat_menu(img):
    # title
    cv2.putText(img, 'STATISTIQUES', (283, 60), cv2.FONT_HERSHEY_COMPLEX, 1, yellow, 2)

    #draw return button
    cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), gray, -1)  
    cv2.putText(img, "RETOUR", (35, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Retour2":
            cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), black, 2)  



# Affichage du menu
cv2.namedWindow("Menu")
cv2.setMouseCallback("Menu", mouse_event)

showWindow = True
while showWindow:

    # Créer une copie de la frame pour chaque itération
    main_menu = background_main.copy()
    lbd_menu = background_lbd.copy()

    #draw buttons 
    if state == "main_menu":
        draw_main_menu(main_menu)
        cv2.imshow("Menu", main_menu)

    elif state == "leaderboard":
        draw_leaderboard(lbd_menu)
        cv2.imshow("Menu", lbd_menu)

    elif state == "statistiques":
        draw_stat_menu(lbd_menu)
        cv2.imshow("Menu", lbd_menu)

    # Attendre une touche pour quitter
    if cv2.waitKey(100) & 0xFF == 27:  # Touche Échap, 100 ms pour changer de frame
        break

