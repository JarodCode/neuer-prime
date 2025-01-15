import cv2
import numpy as np
from PIL import Image, ImageSequence
import subprocess

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
xy_jouer = [300, 500, 200, 260]
xy_leaderboard = [250, 550, 300, 360]
xy_quitter = [300, 500, 400, 460]
xy_retour_lbd = [0, 200, 540, 600]

# Chemin vers le GIF animé
background_path = "neuer-frimpong.gif"

# Chargement du GIF animé avec Pillow
gif = Image.open(background_path)
frames = [cv2.cvtColor(np.array(frame.convert("RGB")), cv2.COLOR_RGB2BGR) for frame in ImageSequence.Iterator(gif)]

# Redimensionnement des frames si nécessaire
window_width, window_height = 800, 600  # Taille de la fenêtre
frames = [cv2.resize(frame, (window_width, window_height)) for frame in frames]

img_lbd_path = "neuer_prime.jpg"
background_lbd = cv2.imread(img_lbd_path)
background_lbd = cv2.resize(background_lbd, (window_width, window_height))

#initial state
state = "main_menu"

# Fonction pour détecter les clics sur les boutons
def mouse_event(event, x, y, flags, param):
    global state  # Déclare que vous utilisez la variable globale "state"
    if event == cv2.EVENT_LBUTTONDOWN:
        #if in main menu
        if state == "main_menu":
            if xy_jouer[0] <= x <= xy_jouer[1] and xy_jouer[2] <= y <= xy_jouer[3]:  # Bouton "Jouer"
                print("Jouer !")
                subprocess.Popen(["python3", "/home/theo.constantin01/IG3/FASE/neuer_prime/detection_main.py"])

            elif xy_leaderboard[0] <= x <= xy_leaderboard[1] and xy_leaderboard[2] <= y <= xy_leaderboard[3]: # Bouton "Leaderboard"
                print("Affichage du leaderboard")
                state = "leaderboard"
            
            elif xy_quitter[0] <= x <= xy_quitter[1] and xy_quitter[2] <= y <= xy_quitter[3]:  # Bouton "Quitter"
                print("Quitter...")
                cv2.destroyAllWindows()
        
        #if in leaderboard 
        elif state == "leaderboard" : 
            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:     #back button
                print("Retour au menu principal")
                state = "main_menu"

        

# Ajouter les boutons par-dessus l'image de fond
def draw_main_menu(img):
    
    
    # Dessiner le bouton "Jouer"
    cv2.rectangle(img, (xy_jouer[0], xy_jouer[2]), (xy_jouer[1], xy_jouer[3]), blue, -1)  
    cv2.putText(img, "JOUER", (350, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    # Dessiner le bouton "Leaderboard"
    cv2.rectangle(img, (xy_leaderboard[0], xy_leaderboard[2]), (xy_leaderboard[1], xy_leaderboard[3]), orange, -1)  
    cv2.putText(img, "LEADERBOARD", (285, 340), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    # Dessiner le bouton "Quitter"
    cv2.rectangle(img, (xy_quitter[0], xy_quitter[2]), (xy_quitter[1], xy_quitter[3]), red, -1) 
    cv2.putText(img, "QUITTER", (332, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

def draw_leaderboard(img):
    
    cv2.putText(img, 'LEADERBOARD', (285, 60), cv2.FONT_HERSHEY_COMPLEX, 1, black, 2)
    
    #draw return button
    cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), gray, -1)  
    cv2.putText(img, "RETOUR", (35, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

# Affichage du menu
cv2.namedWindow("Menu")
cv2.setMouseCallback("Menu", mouse_event)

frame_index = 0
while True:
    # Sélectionner la frame courante
    background = frames[frame_index]
    frame_index = (frame_index + 1) % len(frames)

    # Créer une copie de la frame pour chaque itération
    menu = background.copy()
    lbd_menu = background_lbd.copy()

    #draw buttons 
    if state == "main_menu":
        draw_main_menu(menu)
        cv2.imshow("Menu", menu)

    elif state == "leaderboard":
        draw_leaderboard(lbd_menu)
        cv2.imshow("Menu", lbd_menu)

    # Attendre une touche pour quitter
    if cv2.waitKey(100) & 0xFF == 27:  # Touche Échap, 100 ms pour changer de frame
        break

cv2.destroyAllWindows()
