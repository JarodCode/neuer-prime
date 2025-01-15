import cv2
import numpy as np
from PIL import Image, ImageSequence
import subprocess

# Chemin vers le GIF animé
background_path = "giphy.gif"

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

        elif 300 <= x <= 500 and 300 <= y <= 360:  # Bouton "Quitter"
            print("Quitter...")
            cv2.destroyAllWindows()

# Ajouter les boutons par-dessus l'image de fond
def draw_buttons(img):
    # Dessiner le bouton "Jouer"
    cv2.rectangle(img, (300, 200), (500, 260), (0, 255, 0), -1)  # Vert (rempli)
    cv2.putText(img, "Jouer", (340, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Dessiner le bouton "Quitter"
    cv2.rectangle(img, (300, 300), (500, 360), (0, 0, 255), -1)  # Rouge (rempli)
    cv2.putText(img, "Quitter", (330, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

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
