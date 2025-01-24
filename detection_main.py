import cv2
import mediapipe as mp
import numpy as np
import math
from screeninfo import get_monitors

# Chargement de l'image des gants
glove_img = cv2.imread("img/gant.png", cv2.IMREAD_UNCHANGED)  # Chargement avec canal alpha
if glove_img is None:
    print("Erreur : Impossible de charger l'image 'gant.png'.")
    exit()

# Initialisation de Mediapipe
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
Hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1)

# Récupérer les dimensions de l'écran principal
monitor = get_monitors()[0]  # On suppose qu'on travaille avec l'écran principal
screen_width = monitor.width
screen_height = monitor.height

def overlay_rotated_image(background, overlay, x, y, angle, alpha_mask):
    """Superpose une image avec rotation et transparence sur une autre image."""
    h, w = overlay.shape[:2]

    # Calcul de la matrice de rotation
    rotation_matrix = cv2.getRotationMatrix2D((w // 2, h // 2), -angle, 1.0)

    # Appliquer la rotation à l'image et au masque alpha
    rotated_overlay = cv2.warpAffine(overlay, rotation_matrix, (w, h))
    rotated_alpha = cv2.warpAffine(alpha_mask, rotation_matrix, (w, h))

    # Définir les limites du cadre pour la superposition
    x1, x2 = max(0, x - w // 2), min(background.shape[1], x + w // 2)
    y1, y2 = max(0, y - h // 2), min(background.shape[0], y + h // 2)
    overlay_x1, overlay_x2 = max(0, w // 2 - x), w - max(0, x + w // 2 - background.shape[1])
    overlay_y1, overlay_y2 = max(0, h // 2 - y), h - max(0, y + h // 2 - background.shape[0])

    # Superposition des pixels avec rotation
    blend_area = background[y1:y2, x1:x2]
    rotated_overlay_area = rotated_overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
    rotated_alpha_area = rotated_alpha[overlay_y1:overlay_y2, overlay_x1:overlay_x2][:, :, None]
    background[y1:y2, x1:x2] = rotated_alpha_area * rotated_overlay_area + (1 - rotated_alpha_area) * blend_area

cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)  # Créer la fenêtre avec la propriété de plein écran
cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Passer la fenêtre en plein écran

while True:
    success, img = cap.read()
    if not success:
        print("Erreur : Impossible de lire l'image depuis la webcam.")
        break

    # Redimensionner l'image capturée pour qu'elle remplisse l'écran
    img = cv2.resize(img, (screen_width, screen_height))


    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = Hands.process(imgRGB)

    if result.multi_hand_landmarks:
        for hand_index, handLms in enumerate(result.multi_hand_landmarks):
            h, w, c = img.shape

            # Déterminer si la main est gauche ou droite
            handedness = result.multi_handedness[hand_index].classification[0].label
            is_right_hand = handedness == "Right"  # Si la main est droite

            # Récupération des points pour le poignet (id 0) et le centre de la main (id 9)
            wrist = handLms.landmark[0]
            center_hand = handLms.landmark[9]

            # Coordonnées des points
            cx1, cy1 = int(wrist.x * w), int(wrist.y * h)
            cx2, cy2 = int(center_hand.x * w), int(center_hand.y * h)

            # Calcul de l'angle de rotation
            angle = math.degrees(math.atan2(cy2 - cy1, cx2 - cx1))

            # Calcul du nouvel offset pour positionner le gant au centre de la main
            glove_h, glove_w = glove_img.shape[:2]
            new_width = int(w * 0.3)
            new_height = int(new_width * glove_h / glove_w)
            resized_glove = cv2.resize(glove_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

            if is_right_hand:
                resized_glove = cv2.flip(resized_glove, 1)  # Flip horizontal pour la main droite

            # Récupérer les canaux alpha et BGR
            resized_alpha = resized_glove[:, :, 3] / 255.0
            resized_glove_bgr = resized_glove[:, :, :3]

            # Déplacer le gant pour que son centre soit aligné avec la main
            cx, cy = cx2, cy2  # Utilisation du centre de la main pour le placement

            overlay_rotated_image(img, resized_glove_bgr, cx, cy, angle + 90 , resized_alpha)
            """
            # Dessine les landmarks de la main
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            """
    cv2.imshow("Frame", img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()