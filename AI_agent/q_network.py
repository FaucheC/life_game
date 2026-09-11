import torch.nn as nn



class QNetwork(nn.Module):
    """
    Réseau de neurones qui prend un état en entrée et prédit
    la valeur Q pour chaque action possible
    
    """

    def __init__(self, state_dim = 28, action_dim = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
        )

    def forward(self, x):
        """Retourne les Q-valeurs pour chaque action."""
        return self.net(x)