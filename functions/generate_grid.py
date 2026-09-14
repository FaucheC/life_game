import numpy as np
import random

def grille_aleatoire(lignes, colonnes, probabilite_vivante=0.2):
    """
    Génère une grille de cellules aléatoires.
    Parameters:
    -----------
    probabilite_vivante : float, optionnel (par défaut 0.2)
        Probabilité qu'une cellule soit vivante (1) au départ.
    Returns:
    --------
    numpy.ndarray
        Une grille de dimensions (LIGNES, COLONNES) avec des 0 (mort) et des 1 (vivant).
    """
    #création de la gris aléatoire
    random_grid = np.random.choice([0, 1], size=(lignes, colonnes), p=[1 - probabilite_vivante, probabilite_vivante])

    #ajout de la nourriture   (self.colonnes * self.lignes) - 1 x,y colonne ligne
    for n in range(1, 10):
        x,y = random.randint(1, colonnes-1), random.randint(1, lignes-1)
        random_grid[y][x] = 2

    return random_grid