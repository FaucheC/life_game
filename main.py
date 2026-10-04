import pygame
import numpy as np
import sys
#from functions.generate_grid import grille_aleatoire
from functions.death_grid import grille_vide
from functions.show_grids import afficher_grille
from functions.gerer_clic import gerer_clic
from functions.generate_grid import grille_aleatoire
from functions.load_state import load_state
from functions.save_state import save_state
from grids.environnement import Environnement
from AI_agent.replay_buffer import ReplayBuffer



if __name__ == "__main__":
    # --- Constantes de l'affichage ---
    LARGEUR, HAUTEUR = 800, 800
    TAILLE_CELLULE = 100
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


    load = True
    pause = True  # La simulation est en pause par défaut
    running = True

    # --- Configuration initiale ---
    grille = grille_aleatoire(LIGNES, COLONNES, 0.2)
    Env = Environnement(grille, largeur = 800, hauteur = 800, taille_cellule = 100, load = load)


    # Paramètres et mémoire utilisés pendant l'apprentissage.
    replay_buffer = ReplayBuffer(capacity=10_000)
    batch_size = 64
    epsilon = 1.0
    epsilon_min = 0.05
    epsilon_decay = 0.995



    # --- Boucle principale ---
    while running:
        ecran.fill(NOIR)

        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #sauvegarde du moodèle ici
                Env.agent.save()
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                if event.key == pygame.K_s:
                    save_state(grille)
                if event.key == pygame.K_r:
                    grille = grille_aleatoire(0.2)
                if event.key == pygame.K_c:
                    grille = grille_vide(LIGNES, COLONNES)
                if event.key == pygame.K_RETURN:
                    grille = Env.prochaine_generation(dx = -1, dy = -1)  # pas à pas
                if event.key == pygame.K_UP:
                    grille = Env.prochaine_generation(dx = 0, dy = -1)
                if event.key == pygame.K_DOWN:
                    grille = Env.prochaine_generation(dx = 0, dy = 1)
                if event.key == pygame.K_LEFT:
                    grille = Env.prochaine_generation(dx = -1, dy = 0)
                if event.key == pygame.K_RIGHT:
                    grille = Env.prochaine_generation(dx = 1, dy = 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic gauche
                    souris_x, souris_y = pygame.mouse.get_pos()
                    gerer_clic(souris_x, souris_y, Env.taille_cellule, Env.lignes, Env.colonnes, Env.grille, clic="gauche")

                if event.button == 3:  #clic droit
                    souris_x, souris_y = pygame.mouse.get_pos()
                    gerer_clic(souris_x, souris_y, Env.taille_cellule, Env.lignes, Env.colonnes, Env.grille, clic="droit")

        # --- Mise à jour de la simulation ---
        if not pause:
            agent = Env.agent

            # Garde l'état avant l'action, car l'environnement modifie la grille.
            state = agent.build_state_tensor(Env.grille).squeeze(0).numpy().copy()
            action_id, reward = agent.action(Env, Env.grille, epsilon)
            next_state = agent.build_state_tensor(Env.grille).squeeze(0).numpy().copy()

            # Une énergie insuffisante termine l'épisode; on la restaure ensuite.
            done = agent.energie < 0.5
            replay_buffer.push(state, action_id, reward, next_state, done)

            # update attend d'avoir au moins un batch complet dans la mémoire.
            agent.update(replay_buffer, batch_size=batch_size)

            epsilon = max(epsilon_min, epsilon * epsilon_decay)
            if done:
                # Recommence un épisode sans réinitialiser le réseau appris.
                grille = grille_aleatoire(LIGNES, COLONNES, 0.2)
                Env.grille = grille
                resultat = Env.extraire_agents_potentiels(taille_min=2, connectivite=8)
                agent.position = resultat["agents"][0]["cellules"]
                agent.age = 0
                agent.energie = 10

            grille = Env.grille

        # --- Affichage ---
        afficher_grille(Env.grille, Env.lignes, Env.colonnes, Env.taille_cellule, ecran)

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

#TODO: Sauvegardez les poids du réseaux et charger le modèle si nécessaire
