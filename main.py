import pygame
import numpy as np
import sys
from functions.generate_grid import grille_aleatoire
from functions.death_grid import grille_vide
from functions.show_grids import afficher_grille
from grids.environnement import Environnement



if __name__ == "__main__":
    # --- Initialisation Pygame ---
    LARGEUR, HAUTEUR = 900, 600
    
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu de la Vie - Conway")
    horloge = pygame.time.Clock()