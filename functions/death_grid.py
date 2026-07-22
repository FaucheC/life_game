import numpy as np

def grille_vide(LIGNES, COLONNES):
    """
    Crée une grille entièrement composée de cellules mortes.

    Returns:
    --------
    numpy.ndarray
        Une grille de dimensions (LIGNES, COLONNES) remplie de 0.
    """
    return np.zeros((LIGNES, COLONNES), dtype=int)