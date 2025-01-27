import cv2
import mediapipe as mp
import numpy as np
import math
from screeninfo import get_monitors
from Graphics import Graphic, SceneRender
from Tir import Tir
from Ballon import Ballon
import subprocess
import API_Raspberry as API

def overlay_rotated_image(background, overlay, x, y, angle, alpha_mask):
    """Superpose une image avec rotation et transparence sur une autre image."""
    h, w = overlay.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((w // 2, h // 2), -angle, 1.0)

    # Appliquer la rotation à l'image et au masque alpha
    rotated_overlay = cv2.warpAffine(overlay, rotation_matrix, (w, h))
    rotated_alpha = cv2.warpAffine(alpha_mask, rotation_matrix, (w, h))

    # Définir les limites du cadre pour la superposition
    x1, x2 = max(0, x - w // 2), min(background.shape[1], x + w // 2)
    y1, y2 = max(0, y - h // 2), min(background.shape[0], y + h // 2)
    overlay_x1, overlay_x2 = max(0, w // 2 - x), w - max(0, x + w // 2 - background.shape[1])
    overlay_y1, overlay_y2 = max(0, h // 2 - y), h - max(0, y + h // 2 - background.shape[0])

    # Ajuster dynamiquement les dimensions pour éviter les incompatibilités
    blend_h = min(y2 - y1, overlay_y2 - overlay_y1)
    blend_w = min(x2 - x1, overlay_x2 - overlay_x1)
    y1, y2 = y1, y1 + blend_h
    x1, x2 = x1, x1 + blend_w
    overlay_y1, overlay_y2 = overlay_y1, overlay_y1 + blend_h
    overlay_x1, overlay_x2 = overlay_x1, overlay_x1 + blend_w

    # Superposition des pixels avec rotation
    blend_area = background[y1:y2, x1:x2]
    rotated_overlay_area = rotated_overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
    rotated_alpha_area = rotated_alpha[overlay_y1:overlay_y2, overlay_x1:overlay_x2][:, :, None]

    background[y1:y2, x1:x2] = rotated_alpha_area * rotated_overlay_area + (1 - rotated_alpha_area) * blend_area



def main():
    EPSILON = 1
    WIDTH, HEIGHT = 1600, 900
    MIDW, MIDH = WIDTH/2, HEIGHT/2
    GAMELOOP = True
    GAMEOVERLOOP = True

    compt = 0
    attenteBalle = 0
    score = 0

    # buttons coordinate : [min x, max x, min y, max y]

    xy_score = [0, 300, 0, 100]

    # Charger l'image des gants
    glove_img = cv2.imread("img/Gant.png", cv2.IMREAD_UNCHANGED)
    if glove_img is None:
        print("Erreur : Impossible de charger l'image 'gant.png'.")
        exit()


    
    # Initialiser Mediapipe
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    Hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1)

    # Récupérer les dimensions de l'écran principal
    monitor = get_monitors()[0]
    screen_width = monitor.width 
    screen_height = monitor.height

    # Charger l'image de fond personnalisée
    background_img = cv2.imread("img/background.png")
    if background_img is None:
        print("Erreur : Impossible de charger l'image 'background.jpeg'.")
        exit()
    # Redimensionner l'image de fond aux dimensions de l'écran
    background_img = cv2.resize(background_img, (screen_width, screen_height))


    myTir = Tir()

    # Définir le type de tir (au hasard)
    al = np.random.choice([1, 2, 3])
    if al == 1:
        myTir.panenka()
    elif al == 2:
        myTir.effet()
    else:
        myTir.direct()

    # Création du ballon
    balle = Ballon(sprite="img/Ballon.png",
                   idPos=0,
                   pos=(MIDW, MIDH + 100),
                   traj=myTir.traj,
                   rayon=200,
                   enContactGant=False)
    
    RAYONMAX = balle.rayon
    POSDEPART = balle.pos
    balle.resize_graphic(int(RAYONMAX * 0.1))

    render = SceneRender((screen_width, screen_height))

    nbFrame = np.shape(myTir.traj)
    taille = np.linspace(0.1, 1, nbFrame[1])

    while GAMELOOP:
        # Capture de l'image de la webcam
        _, img = cap.read()

        img = cv2.resize(img, (screen_width, screen_height))
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = Hands.process(imgRGB)

        caneva = background_img.copy()        

        render.clear()
        render.add_layer(caneva)

        if attenteBalle > 10:
            render.add_layer(balle.get_graphic(), balle.update())
            balle.resize_graphic(int(RAYONMAX * taille[compt]))
            if compt < len(taille) - 1:
                compt += 1
        else:
            render.add_layer(balle.get_graphic(), POSDEPART)

        output = render.get_image()

        cv2.rectangle(output, (xy_score[0], xy_score[2]), (xy_score[1], xy_score[3]), (0, 165, 255) , -1)
        cv2.rectangle(output, (xy_score[0], xy_score[2]), (xy_score[1], xy_score[3]), (255, 255, 255), 4)  # Contour blanc
  
        cv2.putText(output, "SCORE : " + str(score), (35, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


        # Variables pour vérifier si la balle est arrêtée
        ball_x, ball_y = balle.pos
        ball_radius = balle.rayon
        ball_stopped = False

        # Superposer les gants si des mains sont détectées
        if result.multi_hand_landmarks:
            for hand_index, handLms in enumerate(result.multi_hand_landmarks):
                h, w, c = img.shape

                # Points clés de la main
                wrist = handLms.landmark[0]
                center_hand = handLms.landmark[9]

                # Extraire les coordonnées x et y de center_hand
                center_hand_x = int(center_hand.x * w)  # Coordonnée en pixels
                center_hand_y = int(center_hand.y * h)  # Coordonnée en pixels

                # Vérifier si la balle est dans la hitbox
                if ball_radius == 200 and abs(center_hand_x - (ball_x + RAYONMAX)) <= RAYONMAX and abs(center_hand_y - (ball_y + RAYONMAX)) <= RAYONMAX:
                    ball_stopped = True  # La balle est arrêtée

                # Déterminer si la main est gauche ou droite
                handedness = result.multi_handedness[hand_index].classification[0].label
                is_right_hand = handedness == "Right"

                # Coordonnées des points
                cx1, cy1 = int(wrist.x * w), int(wrist.y * h)
                cx2, cy2 = int(center_hand.x * w), int(center_hand.y * h)

                # Angle de rotation
                angle = math.degrees(math.atan2(cy2 - cy1, cx2 - cx1))

                # Redimensionner les gants
                glove_h, glove_w = glove_img.shape[:2]
                new_width = int(w * 0.25)
                new_height = int(new_width * glove_h / glove_w)
                resized_glove = cv2.resize(glove_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

                if is_right_hand:
                    resized_glove = cv2.flip(resized_glove, 1)

                resized_alpha = resized_glove[:, :, 3] / 255.0
                resized_glove_bgr = resized_glove[:, :, :3]

                overlay_rotated_image(output, resized_glove_bgr, cx2, cy2, angle + 90, resized_alpha)
            

        # Vérifier si la balle est arrêtée ou si c'est un but
        if ball_radius == 200:
            if ball_stopped:
                print("MAIS QUEL ARRÊT !!!!!")
                balle.resize_graphic(int(RAYONMAX * 0.1))
                balle.pos = POSDEPART
                attenteBalle=0
                compt=0
                score += 100
                balle.idPos=0
                # Définir le type de tir (au hasard)
                al = np.random.choice([1, 2, 3])
                if al == 1:
                    myTir.panenka()
                elif al == 2:
                    myTir.effet()
                else:
                    myTir.direct()
                balle.traj = myTir.traj
            else:
                GAMELOOP = False

        cv2.namedWindow("Resultat", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Resultat", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27:
            GAMELOOP = False

        attenteBalle += 1

    cap.release()
    cv2.destroyAllWindows()

    player_name = ""  # Variable pour stocker le nom du joueur
    MAX_NAME_LENGTH = 13  # Limite maximale de caractères pour le nom
    
    # Affichage de l'écran de Game Over
    while GAMEOVERLOOP:
        # Charger l'image de Game Over
        img_gameover_path = "img/gameOver.jpg"
        gameover = cv2.imread(img_gameover_path)
        gameover = cv2.resize(gameover, (screen_width, screen_height))

        # Calculer la largeur du texte "Score: {score}"
        score_text = f"Score: {score}"
        (score_text_width, score_text_height), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_COMPLEX, 2, 2)

        # Position du score 
        x1_score, y1_score = 750, 650  # Coordonnées du rectangle pour le score
        x2_score = x1_score + score_text_width + 50  # Ajuster avec le padding
        y2_score = y1_score + score_text_height + 40  # Hauteur du rectangle

        # Afficher le rectangle du score 
        cv2.rectangle(gameover, (x1_score, y1_score - 10), (x2_score +30, y2_score), (0, 165, 255), -1)  # Rectangle orange
        cv2.rectangle(gameover, (x1_score, y1_score -10), (x2_score +30, y2_score), (255, 255, 255), 4)  # Contour blanc

        # Afficher le texte du score
        cv2.putText(gameover, score_text, (x1_score + 10, y1_score + score_text_height + 10), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)

        # Calculer la largeur du texte "Nom: {player_name}"
        player_text = f"Nom: {player_name}"
        (player_text_width, player_text_height), _ = cv2.getTextSize(player_text, cv2.FONT_HERSHEY_COMPLEX, 2, 2)

        # Position du nom 
        x1_name, y1_name = 750, y2_score + 50  # Coordonnées du rectangle pour le nom
        x2_name = x1_name + player_text_width + 50  # Ajuster avec le padding
        y2_name = y1_name + player_text_height + 40  # Hauteur du rectangle

        # Dessiner le rectangle du nom
        cv2.rectangle(gameover, (x1_name, y1_name -10 ), (x2_name, y2_name), (0, 165, 255), -1)  # Rectangle orange
        cv2.rectangle(gameover, (x1_name, y1_name -10 ), (x2_name, y2_name), (255, 255, 255), 4)  # Contour blanc

        # Afficher le texte du nom
        cv2.putText(gameover, player_text, (x1_name + 10, y1_name + player_text_height + 10), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)

        # Afficher l'écran de Game Over
        cv2.namedWindow("Game Over", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Game Over", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Game Over", gameover)

        # Capturer les touches clavier
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            GAMEOVERLOOP = False
        elif key == 13:  # Touche 'Entrée'
            if player_name:
                print(f"Nom: {player_name} | Score: {score}")
                API.dweet_for("score", {"name": player_name, "score": score})                
                GAMEOVERLOOP = False
        elif key == 8:  # Touche 'Backspace'
            player_name = player_name[:-1]
        elif key >= 32 and key <= 126:  # Touche visible
            if len(player_name) < MAX_NAME_LENGTH:
                player_name += chr(key)


if __name__ == "__main__":
    main()