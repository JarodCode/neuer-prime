import cv2
import numpy as np

# Chemin vers l'image de fond
background_path = "neuer_prime.jpg"

# Chargement de l'image de fond
background = cv2.imread(background_path)
if background is None:
    raise FileNotFoundError(f"Erreur : Impossible de charger l'image de fond '{background_path}'.")

# Redimensionnement de l'image de fond si nécessaire
window_width, window_height = 800, 600  # Taille de la fenêtre
background = cv2.resize(background, (window_width, window_height))

# Fonction pour détecter les clics sur les boutons
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Vérifiez si le clic est sur un bouton
        if 300 <= x <= 500 and 200 <= y <= 260:  # Bouton "Jouer"
            print("Jouer !")
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

while True:
    # Créer une copie de l'image de fond pour chaque itération
    menu = background.copy()

    # Dessiner les boutons
    draw_buttons(menu)

    # Afficher l'image
    cv2.imshow("Menu", menu)

    # Attendre une touche pour quitter
    if cv2.waitKey(1) & 0xFF == 27:  # Touche Échap
        break

cv2.destroyAllWindows()
