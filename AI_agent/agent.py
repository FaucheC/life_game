

class Agent(object):
    """
    This is class create an Agent who follow rules of life game (see Readme.md)
    """

    def __init__(self, position: tuple, age: int, energie: int):

        self.position = position
        self.age = age
        self.energie = energie


    def choose_action(self, observation):
        """
        Cette fonction choisit l'action a effectuer à partir du réseau de neurones
        """

    def update(self):
        """
        This function update the Deep Q-Network of the agent
        """

    def action(self):
        """
        Cette fonction permet d'envoyer l'action choisit à l'environnement pour obtenir les conséquences 
        """
        