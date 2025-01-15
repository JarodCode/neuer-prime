import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Tir import Tir
from Ballon import Ballon

def main():
    EPSILON = 30
    WIDTH, HEIGHT = 1000, 600

    myTir = Tir()

    # Création du ballon 
    balle = Ballon(sprite="ballon.png",
                   idPos=0,
                   pos=(0,0,0),
                   traj=myTir.panenka(),
                   rayon=50,
                   enContactGant=False)
    
    cap = cv2.VideoCapture(0)

    render = SceneRender((WIDTH,HEIGHT))

    while True:
        caneva = Graphic((WIDTH, HEIGHT))
        caneva.fill((255, 255, 255))

        render.clear()
        render.add_layer(caneva)
        render.add_layer(balle.get_graphic(),balle.update())

        output = render.get_image()
        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
