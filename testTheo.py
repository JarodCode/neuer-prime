import cv2
import numpy as np
import subprocess

# Dimensions de la fenêtre
window_width, window_height = 640, 480

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
blue = (255, 0, 0)
red = (0, 0, 255)

# Boutons avec leurs coordonnées
buttons = {
    "Jouer": ((200, 150), (440, 200), blue),
    "Quitter": ((200, 250), (440, 300), red),
}

# Gestionnaire d'événements de la souris
def mouse_event(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
        for label, ((x1, y1), (x2, y2), _) in buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                if label == "Jouer":
                    print("Lancer le jeu...")
                    # Lancer le script du jeu
                    subprocess.Popen(["python3", "/home/theo.constantin01/IG3/FASE/neuer_prime/detection_main.py"])
                elif label == "Quitter":
                    running = False

# Créer la fenêtre
cv2.namedWindow("Menu")
cv2.setMouseCallback("Menu", mouse_event)

# Variable pour contrôler la boucle principale
running = True

while running:
    # Image de fond
    frame = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255

    # Dessiner les boutons
    for label, ((x1, y1), (x2, y2), color) in buttons.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.putText(frame, label, (x1 + 20, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 2, cv2.LINE_AA)

    # Afficher le menu
    cv2.imshow("Menu", frame)

    # Vérifier si la touche 'q' est pressée pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
