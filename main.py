import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Tir import Tir
from Ballon import Ballon
from screeninfo import get_monitors

def main():

    monitor = get_monitors()[0]

    EPSILON = 1
    WIDTH, HEIGHT = 1600, 900

    myTir = Tir()
    
    al = np.random.choice([1,2,3]) 
    if al == 1 :
        myTir.panenka()
    elif al == 2:
        myTir.effet()
    else: 
        myTir.direct()

    # Création du ballon 
    balle = Ballon(sprite="ballon.png",
                   idPos=0,
                   pos=(0,0),
                   traj=myTir.traj,
                   rayon=50,
                   enContactGant=False)

    render = SceneRender((WIDTH,HEIGHT))

    nbFrame = np.shape(myTir.traj)
    taille = np.linspace(0, 1, nbFrame[0])
    compt = 0
    print(taille[compt])

    while True:
        caneva = Graphic((WIDTH, HEIGHT))
        caneva.fill((50, 205, 50))

        render.clear()

        render.add_layer(caneva)
        render.add_layer(balle.get_graphic(),balle.update())
        ballon_image = cv2.imread(balle.sprite, cv2.IMREAD_UNCHANGED)
        ballon_image = cv2.resize(ballon_image, dsize=None, fx=taille[compt], fy=taille[compt])
        balle.sprite = "temp_image.png"  # Sauvegarde temporaire, si requis
        cv2.imwrite(balle.sprite, ballon_image) 

        output = render.get_image()

        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27: 
            break

        compt += 1

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
