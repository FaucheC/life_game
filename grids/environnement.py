import numpy as np
import random
from collections import deque
from AI_agent.agent import Agent
#from functions.compter_agent import extraire_agents_potentiels

class Environnement(object):
    """
    uniquement np.array

    """

    def __init__(self, grille, largeur = 900, hauteur = 600, taille_cellule = 5):

        self.grille = grille
        self.largeur, self.hauteur = largeur, hauteur
        self.colonnes = self.largeur // taille_cellule
        self.lignes = self.hauteur // taille_cellule
        self.taille_cellule = taille_cellule
        self.nbr_agent = []


    def compter_voisins(self, x, y):
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
                ligne = (x + i) % self.lignes  # bord toroïdal en lignes
                colonne = (y + j) % self.colonnes  # bord toroïdal en colonnes
                somme += self.grille[ligne][colonne]
        return somme

    

    def prochaine_generation(self, dx = 0, dy = 0):
        """
        Calcule la génération suivante selon les règles de Conway,
        puis élimine les amas de cellules vivantes de moins de 5 cellules.

        Règles de Conway :
            - Une cellule vivante avec 2 ou 3 voisins survit.
            - Une cellule vivante avec moins de 2 ou plus de 3 voisins meurt.
            - Une cellule morte avec exactement 3 voisins naît.

        Ensuite, seuls les amas (composantes connexes) de 5 cellules ou plus sont conservés.

        Parameters:
        -----------
        grille : numpy.ndarray
            La grille de cellules actuelle.

        Returns:
        --------
        numpy.ndarray
            La nouvelle grille après application des règles et filtrage des amas.
        """
        # 1. Appliquer les règles de Conway classiques
        #nouvelle = np.copy(grille)
        #for i in range(self.lignes):
        #    for j in range(self.colonnes):
        #        voisins = self.compter_voisins(grille, i, j)
        #        if grille[i][j] == 1:
        #            if voisins < 2 or voisins > 3:
        #                nouvelle[i][j] = 0
        #        else:
        #            if voisins == 3:
        #                nouvelle[i][j] = 1

        # 2. Identifier les amas de 5 cellules ou plus dans la nouvelle grille
        resultat = self.extraire_agents_potentiels(taille_min=5, connectivite=8)

        agent = Agent(resultat["agents"][0]["cellules"], 0, 0)
        self.moove(agent, dx, dy)

        # 3. Construire une grille ne contenant que les cellules des amas survivants
        #grille_finale = np.zeros_like(grille)
        #for agent in resultat["agents"]:
        #    for (i, j) in agent["cellules"]:
        #        grille_finale[i][j] = 1

        #return grille_finale

        return self.grille


######################################################################################

    def extraire_agents_potentiels(self, taille_min=5, connectivite=8):
        """
        Identifie les agents potentiels dans une grille du Jeu de la Vie modifié.

        Un agent potentiel est une composante connexe de cellules vivantes (valeur 1)
        dont la taille est supérieure ou égale à `taille_min`.

        Paramètres
        ----------
        grille : np.ndarray ou liste de listes
            Grille 2D binaire (1 = cellule vivante, 0 = cellule morte).
        taille_min : int, défaut 5
            Nombre minimum de cellules pour former un agent.
        connectivite : int, défaut 8
            4 pour une connexion orthogonale (haut/bas/gauche/droite).
            8 pour une connexion incluant les diagonales.

        Retour
        ------
        dict
            {
                "nombre_agents": int,
                "agents": [
                    {
                        "cellules": [(i, j), ...],
                        "taille": int,
                        "centre": (float, float),   # centre de masse (ligne, colonne)
                        "bbox": (min_i, max_i, min_j, max_j)
                    },
                    ...
                ]
            }
        """
        #grille = np.asarray(grille)

        if self.grille.ndim != 2:
            raise ValueError("La grille doit être 2D.")

        n_lignes, n_colonnes = self.grille.shape
        visite = np.zeros_like(self.grille, dtype=bool)

        if connectivite == 8:
            voisins = [(-1, -1), (-1, 0), (-1, 1),
                       (0, -1),           (0, 1),
                       (1, -1),  (1, 0),  (1, 1)]
        elif connectivite == 4:
            voisins = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            raise ValueError("connectivite doit être 4 ou 8.")

        agents = []

        for i in range(n_lignes):
            for j in range(n_colonnes):
                if self.grille[i, j] == 1 and not visite[i, j]:
                    # BFS pour trouver toute la composante connexe
                    composante = []
                    file = deque()
                    file.append((i, j))
                    visite[i, j] = True

                    while file:
                        ci, cj = file.popleft()
                        composante.append([ci, cj])

                        for di, dj in voisins:
                            ni, nj = ci + di, cj + dj
                            if 0 <= ni < n_lignes and 0 <= nj < n_colonnes:
                                if self.grille[ni, nj] == 1 and not visite[ni, nj]:
                                    visite[ni, nj] = True
                                    file.append((ni, nj))

                    if len(composante) >= taille_min:
                        lignes = [c[0] for c in composante]
                        colonnes = [c[1] for c in composante]
                        centre = (sum(lignes) / len(composante),
                                  sum(colonnes) / len(composante))
                        bbox = (min(lignes), max(lignes), min(colonnes), max(colonnes))
                        agents.append({
                            "cellules": composante,
                            "taille": len(composante),
                            "centre": centre,
                            "bbox": bbox
                        })

        return {
            "nombre_agents": len(agents),
            "agents": agents
        }


    def create_agent(self):
        """
        fonction servant à créer les agents si l'assemblage de cellule le permet
        """

    ########## Partie de l'environnement spécifique aux actions de l'agent #########################################

    def get_observation(self):
        """
        Vision de l'agent
        """

    def moove(self, agent, dx = 1, dy = 1):
        """
        Déplace l'agent
        """
        #TODO: mettre des conditions si la valeurs de x ou y sors de la grille

        ancienne_position = [tuple(cellule) for cellule in agent.position]
        ancienne_position_set = set(ancienne_position)
        nouvelle_position = [
            (ligne + dy, colonne + dx)
            for ligne, colonne in ancienne_position
        ]
        nouvelle_position_set = set(nouvelle_position)

        if any(
            ligne < 0 or ligne >= self.grille.shape[0]
            or colonne < 0 or colonne >= self.grille.shape[1]
            for ligne, colonne in nouvelle_position
        ):
            raise ValueError("Le déplacement sort des limites de la grille")

        for ligne, colonne in ancienne_position_set - nouvelle_position_set:
            self.grille[ligne, colonne] = 0

        for ligne, colonne in nouvelle_position_set:
            self.grille[ligne, colonne] = 1

        agent.position = [[ligne, colonne] for ligne, colonne in nouvelle_position]

        #return grille



    def fight(self, agent_1, agent_2):
        """
        l'agent attaque unn autre agent pour essayer d'obtenir de la nourriture
        """

    def reproduce(self, agent):
        """
        l'agent se reproduit si son niveau d'énergie le lui permet
        """

        if agent.energie > 1000000:
            pass


#TODO: modifier grille pour en faire un attribut global de la classe (1000 fois plus cohérent)
#charger une map vide avec un seul agent et une nourriture