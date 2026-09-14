import numpy as np

def save_state(self, grille, path = "C:/A_Personnel/life_game/utils/grille.npy"):
    """
    Cette fonction sers à sauvegarder l'état de la grille du life game
    """
    np.save(path, grille)