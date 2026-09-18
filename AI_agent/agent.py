from AI_agent.q_network import QNetwork
import random
import torch


class Agent(object):
    """
    This is class create an Agent who follow rules of life game (see Readme.md)
    """

    def __init__(self, position: list, age: int, energie: int):

        self.position = position
        self.age = age
        self.energie = energie


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
                state_t = torch.tensor(grille, dtype=torch.float32).unsqueeze(0)
                q_values = self.q_network(state_t)
                return q_values.argmax().item()
            

        


    def update(self):
        """
        This function update the Deep Q-Network of the agent
        """

    def action(self):
        """
        Cette fonction permet d'envoyer l'action choisit à l'environnement pour obtenir les conséquences 
        """
        