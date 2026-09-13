import pygame
import numpy as np
import sys
#from functions.generate_grid import grille_aleatoire
#from functions.death_grid import grille_vide
from functions.show_grids import afficher_grille
from functions.gerer_clic import gerer_clic
from grids.environnement import Environnement



if __name__ == "__main__":
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

    #initialisation de l'environnement
    Env = Environnement(largeur = 900, hauteur = 600, taille_cellule = 5)

    # --- Configuration initiale ---
    grille = Env.grille_aleatoire(0.2)
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
                if event.key == pygame.K_s:
                    Env.save_state(grille)
                if event.key == pygame.K_r:
                    grille = Env.grille_aleatoire(0.2)
                if event.key == pygame.K_c:
                    grille = Env.grille_vide()
                if event.key == pygame.K_RETURN:
                    grille = Env.prochaine_generation(grille)  # pas à pas

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic gauche
                    souris_x, souris_y = pygame.mouse.get_pos()
                    gerer_clic(souris_x, souris_y, Env.taille_cellule, Env.lignes, Env.colonnes, grille, clic="gauche")

                if event.button == 3:  #clic droit
                    souris_x, souris_y = pygame.mouse.get_pos()
                    gerer_clic(souris_x, souris_y, Env.taille_cellule, Env.lignes, Env.colonnes, grille, clic="droit")

        # --- Mise à jour de la simulation ---
        if not pause:
            grille = Env.prochaine_generation(grille)

        # --- Affichage ---
        afficher_grille(grille, Env.lignes, Env.colonnes, Env.taille_cellule, ecran)

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


#TODO: instancier une classe pour chaque tas de cellule avec également leurs coordonnées
#modifier les coordonnées de l'agent puis réafficher la carte
#avant chaque déplacement, vérifier que les futurs coordonnées sont toujours dans la  carte