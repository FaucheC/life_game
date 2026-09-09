# life_game
Il s'agit d'une version modifié du jeu de la vie de John Conway


# Objectif
L'objectif de ce projet est de réaliser une simulation d'une version modifier du jeu de la vie de John Conway. Chaque être vivant est contrôlé par renforcement learning et cherche à maximiser ses récompenses citées ci-dessous.

Chaque agent aura une certaine quantité d'énergie disponible. Cette énergie permettera aux agents de pouvoir se déplacer, se reproduire où se battre.
De la "nourriture" sera placé sur la carte. Chaque nourriture rapportera plus de vie a l'agent qui l'aura manger et lui obtiendra plus d'énergie.
Chaque "être vivant" pourra choisir la direction de son déplacement.


# règles et fonctionnement du projet
Chaque agent aura une certaines vision de case autour de lui
Les actions possibles 


# Récompenses de l'IA
Se reproduire: l'agent obtient suffisament d'énergie pour se reproduire -> récompense: 100000000
Manger: l'agent réussi à obtenir de  l'énergie lui permettant différentes actions
Se battre: l'agent se bat et perd des points de vies -> récompense négative
Mourir: l'agent meurt -> récompense négative: -10000000
Son enfant meurt: l'enfant de l'agent meurt -> récompense négative: -10000000000 

