import cv2
import mediapipe as mp
import numpy as np
import math
import API_Raspberry as API
from screeninfo import get_monitors
from Graphics import SceneRender
from Shoot import Shoot
from Ball import Ball

#########################################################################
#### - This file represent the local game, without the leaderboard - ####
#########################################################################

# Superimpose an image on an other image with rotation and trasparency

def overlay_rotated_image(background, overlay, x, y, angle, alpha_mask):
    h, w = overlay.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((w // 2, h // 2), -angle, 1.0)

    # Apply the rotation 
    rotated_overlay = cv2.warpAffine(overlay, rotation_matrix, (w, h))
    rotated_alpha = cv2.warpAffine(alpha_mask, rotation_matrix, (w, h))

    # Define limits
    x1, x2 = max(0, x - w // 2), min(background.shape[1], x + w // 2)
    y1, y2 = max(0, y - h // 2), min(background.shape[0], y + h // 2)
    overlay_x1, overlay_x2 = max(0, w // 2 - x), w - max(0, x + w // 2 - background.shape[1])
    overlay_y1, overlay_y2 = max(0, h // 2 - y), h - max(0, y + h // 2 - background.shape[0])

    # Ajust dynamically the dimensions to avoid incompability
    blend_h = min(y2 - y1, overlay_y2 - overlay_y1)
    blend_w = min(x2 - x1, overlay_x2 - overlay_x1)
    y1, y2 = y1, y1 + blend_h
    x1, x2 = x1, x1 + blend_w
    overlay_y1, overlay_y2 = overlay_y1, overlay_y1 + blend_h
    overlay_x1, overlay_x2 = overlay_x1, overlay_x1 + blend_w

    # Superimpose pixels with rotation
    blend_area = background[y1:y2, x1:x2]
    rotated_overlay_area = rotated_overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
    rotated_alpha_area = rotated_alpha[overlay_y1:overlay_y2, overlay_x1:overlay_x2][:, :, None]

    background[y1:y2, x1:x2] = rotated_alpha_area * rotated_overlay_area + (1 - rotated_alpha_area) * blend_area


def main():
    
    # Get monitor size to define differents positions 

    monitor = get_monitors()[0]
    screen_width = monitor.width 
    screen_height = monitor.height

    # Define global variable

    EPSILON = 1
    WIDTH, HEIGHT = screen_width, screen_height
    MIDW, MIDH = WIDTH/2, HEIGHT/2
    GAMELOOP = True
    GAMEOVERLOOP = False
    player_name = ""
    MAX_NAME_LENGTH = 13 

    # Init a shoot and chose it type randomly
    
    myShoot = Shoot()

    al = np.random.choice([1, 2, 3])
    if al == 1:
        myShoot.panenka()
    elif al == 2:
        myShoot.effet()
    else:
        myShoot.direct()

    # Define a linspace for ball resizing 

    nbFrame = np.shape(myShoot.traj)
    size = np.linspace(0.1, 1, nbFrame[1])

    # Creating a ball
    
    balle = Ball(sprite="img/Ballon.png",
                   idPos=0,
                   pos=(MIDW, MIDH + 100),
                   traj=myShoot.traj,
                   radius=200)
    
    # Define global variable link to Ball    

    RADIUSMAX = balle.radius
    POSSTART = balle.pos

    # Define variable used for iterations

    compt = 0
    waitBall = 0
    score = 0

    # buttons coordinate : [min x, max x, min y, max y]

    xy_score = [0, 300, 0, 100]

    # Load used images 

    glove_img = cv2.imread("img/Gant.png", cv2.IMREAD_UNCHANGED)
    background_img = cv2.imread("img/background.png")

    # Resize background to screen size

    background_img = cv2.resize(background_img, (screen_width, screen_height))
    
    # Init Mediapipe

    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    Hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1)

    # Show the ball with the right size
    
    balle.resize_graphic(int(RADIUSMAX * 0.1))

    # Render the scene with the screen dimensions 

    render = SceneRender((screen_width, screen_height))

    # GAMELOOP = True while the player is playing if he lose then GAMELOOP = False 
    # Iy is where the game code is executed

    while GAMELOOP:

        # Recording camera dimensions, change it size, flip it and convert it colors

        _, img = cap.read()
        img = cv2.resize(img, (screen_width, screen_height))
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # init result

        result = Hands.process(imgRGB)
       
        # init a caneva

        caneva = background_img.copy() 
        render.clear()
        render.add_layer(caneva)

        # update the ball if the ball is shoot else the ball wait and stay at POSSTART
        # when the ball is updating it also iterate the size browser, to resize the ball more and more

        if waitBall > 5:
            render.add_layer(balle.get_graphic(), balle.update())
            balle.resize_graphic(int(RADIUSMAX * size[compt]))
            compt += 1
        else:
            render.add_layer(balle.get_graphic(), POSSTART)

        # init output

        output = render.get_image()

        # Draw the the score in a orange rectangle with white outline in the upper left corner

        cv2.rectangle(output, (xy_score[0], xy_score[2]), (xy_score[1], xy_score[3]), (0, 165, 255) , -1)
        cv2.rectangle(output, (xy_score[0], xy_score[2]), (xy_score[1], xy_score[3]), (255, 255, 255), 4)
        cv2.putText(output, "SCORE : " + str(score), (35, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Init variable to check if the ball is stopped
        
        ball_x, ball_y = balle.pos
        ball_radius = balle.radius
        ball_stopped = False

        # If 1 or more hands are detected superimpose gloves on the image

        if result.multi_hand_landmarks:
            for hand_index, handLms in enumerate(result.multi_hand_landmarks):
                h, w, c = img.shape

                # key points of the hand 

                wrist = handLms.landmark[0]
                center_hand = handLms.landmark[9]

                # Extrate coordinates x and y of the center of the hand

                center_hand_x = int(center_hand.x * w)
                center_hand_y = int(center_hand.y * h)  

                # Determine either is left or right hand

                handedness = result.multi_handedness[hand_index].classification[0].label
                is_right_hand = handedness == "Right"

                # Init coordinates of the center of the hand and the center of the wrist for rotating the gloves, corresponding to the real rotation of the hands

                cx1, cy1 = int(wrist.x * w), int(wrist.y * h)
                cx2, cy2 = int(center_hand.x * w), int(center_hand.y * h)

                # Calculation of the rotation angle 

                angle = math.degrees(math.atan2(cy2 - cy1, cx2 - cx1))

                # Resizing gloves

                glove_h, glove_w = glove_img.shape[:2]
                new_width = int(w * 0.25)
                new_height = int(new_width * glove_h / glove_w)
                resized_glove = cv2.resize(glove_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

                if is_right_hand:
                    resized_glove = cv2.flip(resized_glove, 1)

                resized_alpha = resized_glove[:, :, 3] / 255.0
                resized_glove_bgr = resized_glove[:, :, :3]

                # Check if when the radius of the ball is 200 (when the ball is in the goal) the center of the ball is in the hitbox of the gloves
                # Then change the value of ball_stopped

                if ball_radius == 200 and abs(center_hand_x - (ball_x + RADIUSMAX/2)) <= RADIUSMAX and abs(center_hand_y - (ball_y + RADIUSMAX/2)) <= RADIUSMAX:
                    ball_stopped = True

                # Show the hitbox of the ball and the center of the ball for the first shoot in order to have a better comprehension for the player

                if score == 0 :
                    overlay = output.copy()

                    cv2.circle(output, (center_hand_x, center_hand_y), 200, (0, 255, 0), -1)
                    cv2.circle(output, (int(ball_x + balle.radius/2), int(ball_y + balle.radius/2)), 5, (0, 0, 255), -1)

                    output = cv2.addWeighted(overlay, 0.5, output, 1 - 0.5, 0)

                overlay_rotated_image(output, resized_glove_bgr, cx2, cy2, angle + 90, resized_alpha)
            

        # Check if the ball is stopped or if it is a goal when the ball radius is 200

        if ball_radius == 200:

            # if the ball is stopped all the variable are reset and another shoot is chosen randomly

            if ball_stopped:
                balle.resize_graphic(int(RADIUSMAX * 0.1))
                balle.pos = POSSTART
                waitBall=0
                compt=0
                score += 100
                balle.idPos=0

                al = np.random.choice([1, 2, 3])
                if al == 1:
                    myShoot.panenka()
                elif al == 2:
                    myShoot.effet()
                else:
                    myShoot.direct()

                balle.traj = myShoot.traj
            
            # if the ball get in the goal the game finish and it start the GAMEOVERLOOP which represent the gameover screen
            else:
                GAMELOOP = False
                GAMEOVERLOOP = True

        # Display the window

        cv2.namedWindow("Resultat", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Resultat", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Resultat", output)

        # if "q" or "Escp" are pressed it closed the game 

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27:
            GAMELOOP = False

        # iterat waitBall

        waitBall += 1

    # when the game is closed free cap and close all windows

    cap.release()
    cv2.destroyAllWindows()
    
    # Display gameover window

    while GAMEOVERLOOP:

        # Load gameover window and resize it

        img_gameover_path = "img/gameOver.jpg"
        gameover = cv2.imread(img_gameover_path)
        gameover = cv2.resize(gameover, (screen_width, screen_height))

        # Calculate the size of the text score

        score_text = f"Score: {score}"
        (score_text_width, score_text_height), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_COMPLEX, 2, 2)

        # Score coordinates

        x1_score, y1_score = 750, 650
        x2_score = x1_score + score_text_width + 50
        y2_score = y1_score + score_text_height + 40 

        # Display Score (Orange rectangle, white outline)

        cv2.rectangle(gameover, (x1_score, y1_score - 10), (x2_score +30, y2_score), (0, 165, 255), -1)
        cv2.rectangle(gameover, (x1_score, y1_score -10), (x2_score +30, y2_score), (255, 255, 255), 4)
        cv2.putText(gameover, score_text, (x1_score + 10, y1_score + score_text_height + 10), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2)

        # Display gameover screen

        cv2.namedWindow("Game Over", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Game Over", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Game Over", gameover)

        # Recording keys 

        key = cv2.waitKey(1) & 0xFF

        # if "Escp" is pressed then clos the window

        if key == 27:
            GAMEOVERLOOP = False

if __name__ == "__main__":
    main()