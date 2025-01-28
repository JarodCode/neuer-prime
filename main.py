import cv2
import subprocess
import dataBase

# Colors

black = (0, 0, 0)
blue = (180, 130, 70)
red = (60, 20, 220)
green = (50, 205, 50)
orange = (0, 165, 255)
purple = (219, 112, 147)
gray = (169, 169, 169) 
cyan = (255, 255, 0)      

#buttons coordinates : [min x, max x, min y, max y]

#main menu

xy_jouer_enligne = [50, 380, 100, 160]
xy_jouer_horsligne = [420, 790, 100, 160]
xy_leaderboard = [250, 550, 200, 260]
xy_quitter = [300, 500, 300, 360]

#leaderboard menu

xy_retour_lbd = [0, 200, 540, 600]
xy_stat_lbd = [550, 800, 540, 600]

# Window size

window_width, window_height = 800, 600 

# backgrounds
img_main_path = "img/fond_main3.jpg"
background_main = cv2.imread(img_main_path)
background_main = cv2.resize(background_main, (window_width, window_height))

img_lbd_path = "img/fond_ldb.jpg"
background_lbd = cv2.imread(img_lbd_path)
background_lbd = cv2.resize(background_lbd, (window_width, window_height))

# Main while (show menu)

showWindow = False

# Initial state
state = "main_menu"

# Init variable that inidcate which button to highlight
buttonToHighlight = None

# update the leaderboard 

def update_leaderboard():
    global leaderboard
    leaderboard = dataBase.get_leaderboard()


# Detect clicks on button

def mouse_event(event, x, y, flags, param):
    global buttonToHighlight
    global state
    global showWindow
    
    # if the left click is pressed 

    if event == cv2.EVENT_LBUTTONDOWN:

        # if the click has been made in the main menu

        if state == "main_menu":

            # if the click has been made inside the button "Jouer en ligne", start an online game

            if xy_jouer_enligne[0] <= x <= xy_jouer_enligne[1] and xy_jouer_enligne[2] <= y <= xy_jouer_enligne[3]:
                subprocess.Popen(["python3", "onlineGame.py"])

            # if the click has been made inside the button "Jouer hors ligne", start a local game

            elif xy_jouer_horsligne[0] <= x <= xy_jouer_horsligne[1] and xy_jouer_horsligne[2] <= y <= xy_jouer_horsligne[3]:
                subprocess.Popen(["python3", "localGame.py"])
            
            # if the click has been made inside the button "Leaderboard", shwo the leaderboard

            elif xy_leaderboard[0] <= x <= xy_leaderboard[1] and xy_leaderboard[2] <= y <= xy_leaderboard[3]:
                update_leaderboard()
                state = "leaderboard"
            
            # if the click has been made inside the button "Quitter", close the game 
                            
            elif xy_quitter[0] <= x <= xy_quitter[1] and xy_quitter[2] <= y <= xy_quitter[3]:
                showWindow = False
        
        # if the click has been made in the leaderboard menu
        
        elif state == "leaderboard" : 

            # if the click has been made inside the button "Retour", return to main menu 

            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:
                state = "main_menu"

    
    # Follow mouse movement and to change the button highlights

    elif event == cv2.EVENT_MOUSEMOVE:

        # if in main menu

        if state == "main_menu":
            
            # if the mouse is on the button "Jouer en ligne", highlight the button

            if xy_jouer_enligne[0] <= x <= xy_jouer_enligne[1] and xy_jouer_enligne[2] <= y <= xy_jouer_enligne[3]:
                buttonToHighlight = "Jouer en Ligne"
            
            # if the mouse is on the button "Jouer hors ligne", highlight the button

            elif xy_jouer_horsligne[0] <= x <= xy_jouer_horsligne[1] and xy_jouer_horsligne[2] <= y <= xy_jouer_horsligne[3]:
                buttonToHighlight = "Jouer hors Ligne"
            
            # if the mouse is on the button "Leaderboard", highlight the button     

            elif xy_leaderboard[0] <= x <= xy_leaderboard[1] and xy_leaderboard[2] <= y <= xy_leaderboard[3]:
                buttonToHighlight = "Leaderboard"
            
            # if the mouse is on the button "Quitter", highlight the button
            
            elif xy_quitter[0] <= x <= xy_quitter[1] and xy_quitter[2] <= y <= xy_quitter[3]:
                buttonToHighlight = "Quitter"

            # if the mouse is not on a button, no button is highlighted

            else: 
                buttonToHighlight = None
        
        # if in leaderboard 

        elif state == "leaderboard" : 
            
            # if the mouse is on the button "Retour", highlight the button

            if xy_retour_lbd[0] <= x <= xy_retour_lbd[1] and xy_retour_lbd[2] <= y <= xy_retour_lbd[3]:
                buttonToHighlight = "Retour"
            
            # if the mouse is not on a button, no button is highlighted

            else:
                buttonToHighlight = None


# Add button on the background in the main menu

def draw_main_menu(img):    
    
    # Display "Jouer" button

    cv2.rectangle(img, (xy_jouer_enligne[0], xy_jouer_enligne[2]), (xy_jouer_enligne[1], xy_jouer_enligne[3]), blue, -1)  
    cv2.putText(img, "JOUER EN LIGNE", (75, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Jouer en Ligne":
            cv2.rectangle(img, (xy_jouer_enligne[0], xy_jouer_enligne[2]), (xy_jouer_enligne[1], xy_jouer_enligne[3]), black, 2)
    
    cv2.rectangle(img, (xy_jouer_horsligne[0], xy_jouer_horsligne[2]), (xy_jouer_horsligne[1], xy_jouer_horsligne[3]), blue, -1)  
    cv2.putText(img, "JOUER HORS LIGNE", (450, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Jouer hors Ligne":
            cv2.rectangle(img, (xy_jouer_horsligne[0], xy_jouer_horsligne[2]), (xy_jouer_horsligne[1], xy_jouer_horsligne[3]), black, 2)  
    
    # Display "Leaderboard" button

    cv2.rectangle(img, (xy_leaderboard[0], xy_leaderboard[2]), (xy_leaderboard[1], xy_leaderboard[3]), orange, -1)  
    cv2.putText(img, "LEADERBOARD", (285, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Leaderboard":
            cv2.rectangle(img, (xy_leaderboard[0], xy_leaderboard[2]), (xy_leaderboard[1], xy_leaderboard[3]), black, 2)  


    # Display "Quitter" button 

    cv2.rectangle(img, (xy_quitter[0], xy_quitter[2]), (xy_quitter[1], xy_quitter[3]), red, -1) 
    cv2.putText(img, "QUITTER", (332, 340), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Quitter":
        cv2.rectangle(img, (xy_quitter[0], xy_quitter[2]), (xy_quitter[1], xy_quitter[3]), black, 2) 

global leaderboard

# Add button on the background in the leaderboard menu

def draw_leaderboard(img):
    
    # Display leaderbord scores

    for i, (name, score) in enumerate(leaderboard):
        text = f"{name}: {score}"
        cv2.putText(img, text, (xy_leaderboard[0] + 30, 140 + (i * 104)), cv2.FONT_HERSHEY_COMPLEX, 1, black, 2)    
    
    # Display "Retout" button

    cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), gray, -1)  
    cv2.putText(img, "RETOUR", (35, 580), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    if buttonToHighlight == "Retour":
        cv2.rectangle(img, (xy_retour_lbd[0], xy_retour_lbd[2]), (xy_retour_lbd[1], xy_retour_lbd[3]), black, 2)  
 

# Display the menu

cv2.namedWindow("Neuer Prime")
cv2.setMouseCallback("Neuer Prime", mouse_event)

showWindow = True

# if showWindow = True then the menu is on the screen

while showWindow:

    # Create a copy at each iteration

    main_menu = background_main.copy()
    lbd_menu = background_lbd.copy()

    # Draw buttons 
    if state == "main_menu":
        draw_main_menu(main_menu)
        cv2.imshow("Neuer Prime", main_menu)

    elif state == "leaderboard":
        draw_leaderboard(lbd_menu)
        cv2.imshow("Neuer Prime", lbd_menu)

    # Wait fot "Escp" to be pressed to close the menu
    if cv2.waitKey(100) & 0xFF == 27:
        showWindow = False

