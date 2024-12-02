# Projet MOGPL : optimisation robuste dans l’incertain total

## Prérequis
Les bibliothèques suivantes sont requises :
- `numpy`
- `random`
- `matplotlib`
- `gurobipy`

## Utilisation du programme 
Le programme s'éxecute en appelant la fonctoin main() définie dans le fichier main.py. Pour démarrer le programme, exécutez:
`python main.py`

Une fois le programme lancé une interface utilisateur sera disponible, il est possible de se déplacer dans l'arborescence du projet à partir du terminal.

## Arborescence

1. Linéarisation des critères maxmin et minmax regret:
    1. Résolution de l'exemple 1 (scénarios 1 et 2)
    2. Résolution avec le critère MaxMin de l'exemple 1 (1.1)
    3. Résolution avec le critère MinMax Regret de l'exemple 1 (1.2)
    4. Visualisation des solutions de l'exemple 1 (1.3)
    5. Résolution d'un problème généralisé
    6. Etude de l'évolution du temps de résolution en fonction de n et p pour les critères maxmin et minmax (1.4)

2. Linéarisation des critères maxOWA et minOWA:
    1. Trouver les composantes du vecteur L(2, 9, 6, 8, 5, 4) (2.2)
    2. Résolution exemple 1 avec le critère maxOWA (2.4)
    3. Résolution exemple 1 avec le critère minOWA (2.5)
    4. Etude de l'évolution du temps de résolution en fonction de n et p pour les critères maxOWA et minOWA (2.6)

3. Application à la recherche d'un chemin robuste dans un graphe:
    1. Détermination du plus court chemin des graphes de l'exemple 2 (3.2)
    2. Plus courts chemins et critères (3.3)
    3. Etude de l'évolution du temps de résolution pour les plus courts chemins en fonction du nombre de noeuds et d'arcs des graphes (3.4)
               