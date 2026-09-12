import random
from collections import deque
import numpy as np

class ReplayBuffer:
    """
    Mémoire d'expérience (replay buffer) pour le reinforcement learning.

    Stocke des transitions sous la forme (état, action, récompense, état_suivant, terminé)
    et permet d'échantillonner des mini-batchs aléatoires pour l'apprentissage.

    Paramètres
    ----------
    capacity : int
        Nombre maximum de transitions stockées. Une fois pleine, les plus anciennes
        sont automatiquement supprimées.
    """

    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """
        Ajoute une transition dans la mémoire.

        Paramètres
        ----------
        state : array-like
            L'état observé.
        action : int ou array-like
            L'action effectuée.
        reward : float
            La récompense reçue.
        next_state : array-like
            L'état suivant.
        done : bool
            Indique si l'épisode est terminé.
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """
        Tire un échantillon aléatoire de transitions.

        Paramètres
        ----------
        batch_size : int
            Nombre de transitions à échantillonner.

        Retours
        -------
        tuple de np.ndarray
            (states, actions, rewards, next_states, dones) où chaque élément est
            un tableau numpy de taille (batch_size, ...).
        """
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32)  # 0.0 ou 1.0
        )

    def __len__(self):
        """Retourne le nombre de transitions actuellement stockées."""
        return len(self.buffer)