import cv2
import mediapipe as mp
import math
from screeninfo import get_monitors


class Gants:
    def __init__(self, glove_image_path="img/gant.png"):
        # Chargement de l'image des gants
        self.glove_img = cv2.imread(glove_image_path, cv2.IMREAD_UNCHANGED)
        
        # Initialisation de Mediapipe et de la webcam
        self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.Hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1)

        # Récupérer les dimensions de l'écran principal
        monitor = get_monitors()[0]
        self.screen_width = monitor.width
        self.screen_height = monitor.height

        # Fenêtre en plein écran
        cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    @staticmethod
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

    def process_frame(self, background):
        """Détecte les mains et superpose les gants sur l'image de fond."""
        
        # Capture une image de la webcam
        success, frame = self.cap.read()
        if not success:
            print("Erreur : Impossible de lire l'image depuis la webcam.")
            return background

        # Redimensionne et retourne horizontalement l'image de la webcam
        frame = cv2.resize(frame, (self.screen_width, self.screen_height))
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détecte les mains avec Mediapipe
        result = self.Hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_index, handLms in enumerate(result.multi_hand_landmarks):
                h, w, c = background.shape

                # Détermine si la main est gauche ou droite
                handedness = result.multi_handedness[hand_index].classification[0].label
                is_right_hand = handedness == "Right"

                # Récupère les points pour le poignet (id 0) et le centre de la main (id 9)
                wrist = handLms.landmark[0]
                center_hand = handLms.landmark[9]

                # Coordonnées des points
                cx1, cy1 = int(wrist.x * w), int(wrist.y * h)
                cx2, cy2 = int(center_hand.x * w), int(center_hand.y * h)

                # Calcule l'angle de rotation
                angle = math.degrees(math.atan2(cy2 - cy1, cx2 - cx1))

                # Redimensionne l'image des gants pour s'adapter à la taille de la main
                glove_h, glove_w = self.glove_img.shape[:2]
                new_width = int(w * 0.3)
                new_height = int(new_width * glove_h / glove_w)
                resized_glove = cv2.resize(self.glove_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Retourne horizontalement le gant si la main est droite
                if is_right_hand:
                    resized_glove = cv2.flip(resized_glove, 1)

                # Récupère les canaux alpha et BGR
                resized_alpha = resized_glove[:, :, 3] / 255.0
                resized_glove_bgr = resized_glove[:, :, :3]

                # Positionne le gant sur la main détectée
                self.overlay_rotated_image(background, resized_glove_bgr, cx2, cy2, angle + 90, resized_alpha)

        return background

    


