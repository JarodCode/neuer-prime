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


# Chemin vers le GIF animé
background_path = "neuer-frimpong.gif"

# Chargement du GIF animé avec Pillow
gif = Image.open(background_path)
frames = [cv2.cvtColor(np.array(frame.convert("RGB")), cv2.COLOR_RGB2BGR) for frame in ImageSequence.Iterator(gif)]

# Redimensionnement des frames si nécessaire
window_width, window_height = 800, 600  # Taille de la fenêtre
frames = [cv2.resize(frame, (window_width, window_height)) for frame in frames]

# Fonction pour détecter les clics sur les boutons
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Vérifiez si le clic est sur un bouton
        if 300 <= x <= 500 and 200 <= y <= 260:  # Bouton "Jouer"
            print("Jouer !")
            subprocess.Popen(["python3", "/home/theo.constantin01/IG3/FASE/neuer_prime/detection_main.py"])

        elif 300 <= x <= 500 and 300 <= y <= 360: # Bouton "Leaderboard"
            print("Affichage du leaderboard")
        
        elif 300 <= x <= 500 and 400 <= y <= 460:  # Bouton "Quitter"
            print("Quitter...")
            cv2.destroyAllWindows()

        

# Ajouter les boutons par-dessus l'image de fond
def draw_buttons(img):
    # Dessiner le bouton "Jouer"
    cv2.rectangle(img, (300, 200), (500, 260), blue, -1)  
    cv2.putText(img, "JOUER", (350, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    # Dessiner le bouton "Leaderboard"
    cv2.rectangle(img, (250, 300), (550, 360), orange, -1)  
    cv2.putText(img, "LEADERBOARD", (285, 340), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

    # Dessiner le bouton "Quitter"
    cv2.rectangle(img, (300, 400), (500, 460), red, -1) 
    cv2.putText(img, "QUITTER", (332, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

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

    # Dessiner les boutons
    draw_buttons(menu)

    # Afficher l'image
    cv2.imshow("Menu", menu)

    # Attendre une touche pour quitter
    if cv2.waitKey(100) & 0xFF == 27:  # Touche Échap, 100 ms pour changer de frame
        break

cv2.destroyAllWindows()
