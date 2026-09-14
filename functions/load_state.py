import numpy as np

def load_state(path = "C:/A_Personnel/life_game/utils/grille.npy"):
    """
    Cette fonction permet de charger l'état d'une grille précédente
    """
    grille = np.load(path)

    return grille