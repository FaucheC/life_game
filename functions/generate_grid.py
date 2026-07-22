import numpy as np

def grille_aleatoire(LIGNES, COLONNES, probabilite_vivante=0.2):
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
    return np.random.choice([0, 1], size=(LIGNES, COLONNES), p=[1 - probabilite_vivante, probabilite_vivante])