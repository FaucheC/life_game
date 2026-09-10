import numpy as np

class Environnement(object):
    """
    uniquement np.array

    """

    def __init__(self, largeur = 900, hauteur = 600, taille_cellule = 5):

        self.largeur, self.hauteur = largeur, hauteur
        self.colonnes = self.largeur // taille_cellule
        self.lignes = self.hauteur // taille_cellule
        self.taille_cellule = taille_cellule


    def compter_voisins(self, grille, x, y):
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
                somme += grille[ligne][colonne]
        return somme

    def prochaine_generation(self, grille):
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
        for i in range(self.lignes):
            for j in range(self.colonnes):
                voisins = self.compter_voisins(grille, i, j)
                if grille[i][j] == 1:
                    if voisins < 2 or voisins > 3:
                        nouvelle[i][j] = 0
                else:
                    if voisins == 3:
                        nouvelle[i][j] = 1
        return nouvelle


    def grille_aleatoire(self, probabilite_vivante=0.2):
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
        return np.random.choice([0, 1], size=(self.lignes, self.colonnes), p=[1 - probabilite_vivante, probabilite_vivante])

    def grille_vide(self):
        """
        Crée une grille entièrement composée de cellules mortes.

        Returns:
        --------
        numpy.ndarray
            Une grille de dimensions (LIGNES, COLONNES) remplie de 0.
        """
        return np.zeros((self.lignes, self.colonnes), dtype=int)



    def get_observation(self):
        """
        Vision de l'agent
        """

    def moove(agent, dx, dy):
        """
        Déplace l'agent
        """