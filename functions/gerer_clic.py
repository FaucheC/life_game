import numpy as np

def gerer_clic(souris_x, souris_y, TAILLE_CELLULE, LIGNES, COLONNES, grille, clic):
    """
    Inverse l'état de la cellule cliquée par l'utilisateur.

    Parameters:
    -----------
    souris_x : int
        La coordonnée X de la souris (en pixels).
    souris_y : int
        La coordonnée Y de la souris (en pixels).
    """
    col = souris_x // TAILLE_CELLULE
    ligne = souris_y // TAILLE_CELLULE
    if clic == "gauche":
        if 0 <= ligne < LIGNES and 0 <= col < COLONNES:
            if grille[ligne][col] == 0:
                grille[ligne][col] = 1
            elif grille[ligne][col] == 1:
                grille[ligne][col] = 0
            elif grille[ligne][col] == 2:
                grille[ligne][col] = 0

                
    elif clic == "droit":
        if 0 <= ligne < LIGNES and 0 <= col < COLONNES:
            grille[ligne][col] = 2  