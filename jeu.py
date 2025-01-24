import cv2
import numpy as np
import subprocess
import API_Raspberry
from Graphics import Graphic, SceneRender
from Tir import Tir
from Ballon import Ballon
from Gants import Gants  # Import de la classe Gants
from screeninfo import get_monitors


def main():
    EPSILON = 1
    WIDTH, HEIGHT = 1600, 900
    GAMELOOP = True

    # Initialisation de la classe Gants
    myGants = Gants(glove_image_path="img/gant.png")

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
    balle = Ballon(sprite="ballon.png",
                   idPos=0,
                   pos=(0, 0),
                   traj=myTir.traj,
                   rayon=200,
                   enContactGant=False)

    render = SceneRender((WIDTH, HEIGHT))

    nbFrame = np.shape(myTir.traj)
    taille = np.linspace(0.1, 1, nbFrame[1])
    compt = 0
    RAYON = balle.rayon

    while GAMELOOP:
        caneva = Graphic((WIDTH, HEIGHT))
        caneva.fill((50, 205, 50))

        render.clear()
        balle.resize_graphic(int(RAYON * taille[compt]))
        render.add_layer(caneva)
        render.add_layer(balle.get_graphic(), balle.update())

        output = render.get_image()

        # Appel du traitement des gants
        output_with_gloves = myGants.process_frame(output)

        # Débogage
        cv2.imshow("Output Before Gloves", output)
        cv2.imshow("Processed Frame", output_with_gloves)

        cv2.imshow("Resultat Final", output_with_gloves)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27:
            GAMELOOP = False

        if compt < len(taille) - 1:
            compt += 1

    myGants.cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
