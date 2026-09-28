from AI_agent.q_network import QNetwork
from AI_agent.replay_buffer import ReplayBuffer
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
        self.optimizer = torch.optim.Adam(self.brain.parameters(), lr=1e-3)

    def build_state_tensor(self, grille: np.ndarray) -> torch.Tensor:
        """Construit l'état du réseau à partir de la grille, de la position et de l'énergie.

        La grille doit avoir la forme (8, 8). Les 64 cellules sont suivies des
        coordonnées aplaties des trois cellules de l'agent, puis de son énergie.
        Le tenseur retourné est un batch float32 de forme (1, 71), prêt pour le QNetwork.
        """
        grille_tensor = torch.as_tensor(grille, dtype=torch.float32).reshape(-1)
        position_tensor = torch.as_tensor(self.position, dtype=torch.float32).reshape(-1)

        # Le réseau attend toujours trois coordonnées (6 valeurs), même si
        # l'agent extrait de la grille contient un nombre différent de cellules.
        position_tensor = position_tensor[:6]
        if position_tensor.numel() < 6:
            position_tensor = torch.nn.functional.pad(
                position_tensor, (0, 6 - position_tensor.numel())
            )

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
            # + ajouuter la possibilité de charger le modèle également
            with torch.no_grad():
                state_t = self.build_state_tensor(grille)
                q_values = self.brain(state_t)
                return q_values.argmax(dim=1).item()
            

        


    def update(self, replay_buffer: ReplayBuffer, batch_size: int = 64, gamma: float = 0.99):
        """
        Met à jour le Q-network à partir d'un batch de transitions mémorisées.

        Les états stockés dans le buffer doivent être ceux produits par
        `build_state_tensor`, convertis en tableaux de forme (71,) ou (1, 71).
        Retourne la perte d'apprentissage, ou None si le buffer est trop petit.
        """
        # L'apprentissage attend un batch complet d'expériences.
        if len(replay_buffer) < batch_size:
            return None

        # Échantillonne les transitions puis convertit leurs valeurs en tenseurs.
        states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
        states = torch.as_tensor(states, dtype=torch.float32).reshape(batch_size, -1)
        actions = torch.as_tensor(actions, dtype=torch.int64).reshape(batch_size, 1)
        rewards = torch.as_tensor(rewards, dtype=torch.float32).reshape(batch_size)
        next_states = torch.as_tensor(next_states, dtype=torch.float32).reshape(batch_size, -1)
        dones = torch.as_tensor(dones, dtype=torch.float32).reshape(batch_size)

        # Récupère Q(s, a) pour l'action réellement effectuée dans chaque état.
        current_q_values = self.brain(states).gather(1, actions).squeeze(1)

        # Calcule la cible de Bellman; un état terminal n'a pas de récompense future.
        with torch.no_grad():
            next_q_values = self.brain(next_states).max(dim=1).values
            target_q_values = rewards + gamma * next_q_values * (1 - dones)

        # Réduit l'écart entre Q(s, a) prédit et sa cible, puis met à jour le réseau.
        loss = torch.nn.functional.smooth_l1_loss(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def action(self, environnement, grille: np.ndarray, epsilon: float = 0.0):
        """
        Choisit une action, l'envoie à l'environnement et retourne sa récompense.

        L'action est un entier entre 0 et 3 : haut, bas, gauche ou droite.

        Args:
            environnement: Environnement qui applique l'action de l'agent.
            grille: Grille courante utilisée pour choisir l'action.
            epsilon: Probabilité de choisir une action aléatoire.

        Returns:
            Un tuple contenant l'identifiant de l'action et la récompense obtenue.
        """
        # Choisit une direction, puis laisse l'environnement appliquer son effet.
        action_id = self.choose_action(grille, epsilon)
        reward = environnement.step(action_id)
        
        return action_id, reward
