import numpy as np
import pygame

def afficher_grille(grille, LIGNES, COLONNES, TAILLE_CELLULE, ecran):
    """
    Dessine la grille sur l'écran Pygame.

    Chaque cellule est un petit rectangle de couleur VERT (vivante)
    ou GRIS (morte).

    Parameters:
    -----------
    grille : numpy.ndarray
        La grille à afficher.
    """
    # Couleurs (RVB)
    NOIR = (0, 0, 0)
    BLANC = (255, 255, 255)
    GRIS = (40, 40, 40)
    VERT = (0, 200, 0)
    ROUGE = (200, 0, 0)


    for i in range(LIGNES):
        for j in range(COLONNES):
            couleur = VERT if grille[i][j] == 1 else GRIS
            pygame.draw.rect(ecran, couleur,
                             (j * TAILLE_CELLULE, i * TAILLE_CELLULE,
                              TAILLE_CELLULE - 1, TAILLE_CELLULE - 1))  # -1 pour laisser un espace visuel