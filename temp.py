import cv2

# Charger l'image
img = cv2.imread("img/Gant.png")
if img is None:
    print("Erreur : Impossible de charger 'Ballon.png'.")
    exit()

# Afficher l'image
cv2.namedWindow("Fenetre", cv2.WINDOW_NORMAL)  # Assure la compatibilité avec X11
cv2.imshow("Fenetre", img)

# Attendre une touche pour fermer
cv2.waitKey(0)
cv2.destroyAllWindows()
