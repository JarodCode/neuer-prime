import numpy as np
from Graphics import Graphic, SceneRender
import cv2
from Tir import Tir
from Ballon import Ballon

def main():
    EPSILON = 1
    WIDTH, HEIGHT = 1000, 600

    myTir = Tir()
    myTir.panenkaDroite()

    # Création du ballon 
    balle = Ballon(sprite="ballon2.jpeg",
                   idPos=0,
                   pos=(0, 0),
                   traj=myTir.traj,
                   rayon=50,
                   enContactGant=False)
    
    cap = cv2.VideoCapture(0)

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

        if visible_x_min < visible_x_max and visible_y_min < visible_y_max:
            # Découper le ballon pour l'ajouter au canevas
            caneva.image[visible_y_min:visible_y_max, visible_x_min:visible_x_max] = ballon_display[
                visible_y_min - int(visible_y - r):visible_y_max - int(visible_y - r),
                visible_x_min - int(visible_x - r):visible_x_max - int(visible_x - r)
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
