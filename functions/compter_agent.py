import numpy as np
from collections import deque

def extraire_agents_potentiels(grille, taille_min=5, connectivite=8):
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
    grille = np.asarray(grille)
    if grille.ndim != 2:
        raise ValueError("La grille doit être 2D.")

    n_lignes, n_colonnes = grille.shape
    visite = np.zeros_like(grille, dtype=bool)

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
            if grille[i, j] == 1 and not visite[i, j]:
                # BFS pour trouver toute la composante connexe
                composante = []
                file = deque()
                file.append((i, j))
                visite[i, j] = True

                while file:
                    ci, cj = file.popleft()
                    composante.append((ci, cj))

                    for di, dj in voisins:
                        ni, nj = ci + di, cj + dj
                        if 0 <= ni < n_lignes and 0 <= nj < n_colonnes:
                            if grille[ni, nj] == 1 and not visite[ni, nj]:
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