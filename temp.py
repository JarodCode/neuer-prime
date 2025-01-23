import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Tir import Tir
from Ballon import Ballon

def main():
    EPSILON = 1
    WIDTH, HEIGHT = 1000, 600

    myTir = Tir()


    al = np.random.choice([1,2,3]) 
    if al == 1 :
        myTir.panenka()
    elif al == 2:
        myTir.effet()
    else: 
        myTir.direct()

    # Création du ballon 
    balle = Ballon(sprite="ballon2.jpeg",
                   idPos=0,
                   pos=(0, 0),
                   traj=myTir.traj,
                   rayon=50,
                   enContactGant=False)

    render = SceneRender((WIDTH, HEIGHT))

    while True:
        caneva = Graphic((WIDTH, HEIGHT))
        caneva.fill((255, 255, 255))  # Remplir le canevas avec un fond blanc

        render.clear()

        # Mettre à jour la position du ballon
        balle.update()

        # Charger l'image du ballon directement avec OpenCV
        ballon_image = cv2.imread(balle.sprite, cv2.IMREAD_UNCHANGED)  # Charge en RGBA si disponible

        if ballon_image is None:
            print("Impossible de charger l'image du ballon")
            break
        else:
            print("Image du ballon chargée avec succès")
            print(f"Shape de l'image du ballon : {ballon_image.shape}")

        # Vérification du nombre de canaux de l'image
        if ballon_image.shape[2] == 3:  # Si l'image est en RGB
            print("Conversion en RGBA...")
            ballon_image = cv2.cvtColor(ballon_image, cv2.COLOR_BGR2BGRA)  # Convertir en RGBA

        # Afficher l'image du ballon seule (sans fond)
        print("Affichage de l'image du ballon seule...")
        ballon_display = ballon_image

        # Afficher le canevas avec le ballon
        visible_x, visible_y = balle.pos
        r = balle.rayon

        # S'assurer que les coordonnées sont dans les limites de l'écran
        visible_x_min = max(int(visible_x - r), 0)
        visible_y_min = max(int(visible_y - r), 0)
        visible_x_max = min(int(visible_x + r), WIDTH)
        visible_y_max = min(int(visible_y + r), HEIGHT)

        # Découper la partie visible de l'image du ballon
        ballon_x_min = max(0, int(r - visible_x))  # Partie de l'image qui reste visible
        ballon_y_min = max(0, int(r - visible_y))
        ballon_x_max = min(2 * r, int(r + WIDTH - visible_x))
        ballon_y_max = min(2 * r, int(r + HEIGHT - visible_y))

        if visible_x_min < visible_x_max and visible_y_min < visible_y_max:
            # Ajouter la découpe de l'image du ballon au canevas
            caneva.image[visible_y_min:visible_y_max, visible_x_min:visible_x_max] = ballon_display[
                ballon_y_min:ballon_y_max, ballon_x_min:ballon_x_max
            ]
        else:
            print("Le ballon est hors de l'écran ou mal positionné")

        render.add_layer(caneva)

        output = render.get_image()
        cv2.imshow("Resultat", output)

        key = cv2.waitKey(EPSILON) & 0xFF
        if key == ord('q') or key == 27: 
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
