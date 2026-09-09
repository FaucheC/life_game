"""
Jeu de la Vie de Conway - Simulation Pygame
Auteur : Fauché
Description : Implémentation interactive du Jeu de la Vie avec gestion de la grille,
             contrôle de la simulation (pause, pas à pas) et édition manuelle.
"""

import pygame
import numpy as np
import sys
from functions.generate_grid import grille_aleatoire
from functions.death_grid import grille_vide

# --- Constantes de l'affichage ---
LARGEUR, HAUTEUR = 900, 600
TAILLE_CELLULE = 5
COLONNES = LARGEUR // TAILLE_CELLULE
LIGNES = HAUTEUR // TAILLE_CELLULE

# Couleurs (RVB)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (40, 40, 40)
VERT = (0, 200, 0)
ROUGE = (200, 0, 0)

# --- Initialisation Pygame ---
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de la Vie - Conway")
horloge = pygame.time.Clock()



# --- Fonctions du Jeu de la Vie (mécaniques) ---

def compter_voisins(grille, x, y):
    """
    Compte le nombre de voisins vivants d'une cellule donnée.

    La grille est considérée comme toroïdale : les cellules des bords
    sont connectées aux cellules du côté opposé.

    Parameters:
    -----------
    grille : numpy.ndarray
        La grille de cellules (2D).
    x : int
        L'indice de la ligne de la cellule.
    y : int
        L'indice de la colonne de la cellule.

    Returns:
    --------
    int
        Le nombre de voisins vivants (entre 0 et 8).
    """
    somme = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # ignorer la cellule elle-même
            ligne = (x + i) % LIGNES  # bord toroïdal en lignes
            colonne = (y + j) % COLONNES  # bord toroïdal en colonnes
            somme += grille[ligne][colonne]
    return somme

def prochaine_generation(grille):
    """
    Calcule la génération suivante selon les règles de Conway.

    Règles :
        - Une cellule vivante avec 2 ou 3 voisins survivent.
        - Une cellule vivante avec moins de 2 ou plus de 3 voisins meurt.
        - Une cellule morte avec exactement 3 voisins naît.

    Parameters:
    -----------
    grille : numpy.ndarray
        La grille de cellules actuelle.

    Returns:
    --------
    numpy.ndarray
        La nouvelle grille après application des règles.
    """
    nouvelle = np.copy(grille)
    for i in range(LIGNES):
        for j in range(COLONNES):
            voisins = compter_voisins(grille, i, j)
            if grille[i][j] == 1:
                if voisins < 2 or voisins > 3:
                    nouvelle[i][j] = 0
            else:
                if voisins == 3:
                    nouvelle[i][j] = 1
    return nouvelle

# --- Fonctions d'affichage ---

def afficher_grille(grille):
    """
    Dessine la grille sur l'écran Pygame.

    Chaque cellule est un petit rectangle de couleur VERT (vivante)
    ou GRIS (morte).

    Parameters:
    -----------
    grille : numpy.ndarray
        La grille à afficher.
    """
    for i in range(LIGNES):
        for j in range(COLONNES):
            couleur = VERT if grille[i][j] == 1 else GRIS
            pygame.draw.rect(ecran, couleur,
                             (j * TAILLE_CELLULE, i * TAILLE_CELLULE,
                              TAILLE_CELLULE - 1, TAILLE_CELLULE - 1))  # -1 pour laisser un espace visuel

def gerer_clic(souris_x, souris_y):
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
    if 0 <= ligne < LIGNES and 0 <= col < COLONNES:
        grille[ligne][col] = 1 - grille[ligne][col]  # inverse (0 ↔ 1)

# --- Configuration initiale ---
grille = grille_aleatoire(LIGNES, COLONNES)
pause = True  # La simulation est en pause par défaut
running = True

# --- Boucle principale ---
while running:
    ecran.fill(NOIR)

    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_r:
                grille = grille_aleatoire(LIGNES, COLONNES)
            if event.key == pygame.K_c:
                grille = grille_vide(LIGNES, COLONNES)
            if event.key == pygame.K_RETURN:
                grille = prochaine_generation(grille)  # pas à pas

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # clic gauche
                souris_x, souris_y = pygame.mouse.get_pos()
                gerer_clic(souris_x, souris_y)

    # --- Mise à jour de la simulation ---
    if not pause:
        grille = prochaine_generation(grille)

    # --- Affichage ---
    afficher_grille(grille)

    # --- Affichage des informations (barre d'état) ---
    font = pygame.font.Font(None, 20)
    texte_pause = "PAUSE" if pause else "EN COURS"
    surface_texte = font.render(
        f"Espace: {texte_pause} | R: random | C: effacer | Entrée: pas à pas",
        True, BLANC
    )
    ecran.blit(surface_texte, (10, HAUTEUR - 30))

    pygame.display.flip()
    horloge.tick(10)  # 10 images par seconde (FPS)