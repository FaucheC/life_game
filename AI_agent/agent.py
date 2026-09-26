from AI_agent.q_network import QNetwork
import random
import torch
import numpy as np


class Agent(object):
    """
    This is class create an Agent who follow rules of life game (see Readme.md)
    """

    def __init__(self, position: list, age: int, energie: int):

        self.position = position
        self.age = age
        self.energie = energie

        #création du cerveau
        self.brain = QNetwork(71, 4)

    def build_state_tensor(self, grille: np.ndarray) -> torch.Tensor:
        """Construit l'état du réseau à partir de la grille, de la position et de l'énergie.

        La grille doit avoir la forme (8, 8). Les 64 cellules sont suivies des
        coordonnées aplaties des trois cellules de l'agent, puis de son énergie.
        Le tenseur retourné est un batch float32 de forme (1, 71), prêt pour le QNetwork.
        """
        grille_tensor = torch.as_tensor(grille, dtype=torch.float32).reshape(-1)
        position_tensor = torch.tensor(self.position, dtype=torch.float32).reshape(-1)
        energie_tensor = torch.tensor([self.energie], dtype=torch.float32)
        return torch.cat((grille_tensor, position_tensor, energie_tensor)).unsqueeze(0)


    def choose_action(self, grille, epsilon):
        """
        Cette fonction choisit l'action a effectuer à partir du réseau de neurones
        """
        if random.random() < epsilon:
            #exploration (action aléatoire)
            return random.randrange(0, 4, 1)

        else:
            #TODO: ajouter la partie pour additionner le tableau de la grille et le niveau d'énergie et la position
            # + ajouuter la possibilité de charger le modèle également
            with torch.no_grad():
                state_t = self.build_state_tensor(grille)
                q_values = self.brain(state_t)
                #TODO: modifier le return, je suis presque sur que ça ne marche pas (il suffit juste de récupérer l'action ayant la valeur maximale)
                return q_values.argmax().item()
            

        


    def update(self):
        """
        This function update the Deep Q-Network of the agent
        """

    def action(self):
        """
        Cette fonction permet d'envoyer l'action choisit à l'environnement pour obtenir les conséquences 
        """
        