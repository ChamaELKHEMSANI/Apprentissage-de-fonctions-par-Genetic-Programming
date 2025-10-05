# Genetic Programming Function Learning

Un système de programmation génétique (GP) pour l'apprentissage automatique de fonctions mathématiques, implémenté en Python avec une interface graphique PyQt5.

## Description

Ce projet implémente un algorithme de programmation génétique capable de :
- Découvrir des fonctions mathématiques à partir de données d'entrée/sortie
- Traiter des fonctions à une ou plusieurs variables
- Fournir une interface graphique interactive pour configurer et visualiser les résultats
- Exporter les résultats sous différents formats

## Fonctionnalités

- **Multiples modes d'exécution** : dialogue interactif, ligne de commande, batch
- **Support multi-dimensionnel** : fonctions à 1D, 2D et n-dimensions
- **Interface graphique complète** : visualisation en temps réel, graphes de convergence
- **Algorithmes évolutifs avancés** : sélection, croisement, mutation configurables
- **Visualisation** : arbres d'expression, courbes de fitness, surfaces 3D

## Installation

### Prérequis
- Python 3.7+
- Les dépendances listées dans `requirements.txt`

### Installation des dépendances
```bash
pip install -r requirements.txt



Les principales dépendances incluent :

PyQt5
NumPy
Matplotlib

Utilisation
Mode Interface Graphique (Recommandé)
python main.py -mode "dialogue"

Mode Ligne de Commande

# Apprentissage d'une fonction simple
python main.py -mode "run" -f "x**2+x*sin(x)" -xmin 0 -xmax 10 -s 123 -v 1 -out "data/output.txt"

# Génération de population
python main.py -mode "populate"

# Analyse en 2D
python main.py -mode "2d" -f "sin(x)*x**2+cos(x)*y**2" -xmin 1 -xmax 2 -ymin 1 -ymax 2 -s 123

# Mode batch avec itérations
python main.py -mode "iterate" -f "x**2+x*sin(x)" -xmin 0 -xmax 10 -s 123 -iter_field size_depth -iter_min 4 -iter_max 11 -iter_step 1 -out "data/output_profondeur_4_10.csv" -v

Structure du Projet
├── main.py                 # Point d'entrée principal
├── mainGP.py              # Classe principale de gestion
├── algo/                  # Algorithmes génétiques
│   ├── algoGP.py          # Algorithme principal
│   ├── algoThreadGP.py    # Version threadée
│   ├── chromosomeGP.py    # Représentation des chromosomes
│   └── geneGP.py          # Gènes et opérations
├── dlg/                   # Interface graphique
│   ├── dialogueGP.py      # Dialogue principal
│   ├── dialogueUI.py      # Widgets UI
│   └── treeGP.py          # Visualisation d'arbres
├── tools/                 # Utilitaires
│   ├── argParseToolsGP.py # Parsing des arguments
│   ├── configToolsGP.py   # Gestion de configuration
│   ├── drawToolsGP.py     # Outils de visualisation
│   └── mathsToolsGP.py    # Outils mathématiques
└── data/                  # Données et résultats


Configuration
Paramètres Principaux
size_population : Taille de la population (défaut: 200)
max_depth : Profondeur maximale des arbres (défaut: 5)
max_iterations : Nombre maximum d'itérations (défaut: 20)
size_echantillon : Taille de l'échantillon de sélection
seuil_fitness : Seuil d'arrêt de la fitness

Opérateurs Génétiques
Sélection : best, worst, random
Croisement : middle, absorption partielle/totale
Mutation : replace, swap, déplace
Remplacement : mixt_best, child_only, child_add, mixt_rand

Résultats et Visualisation
Le système génère :
Formules mathématiques simplifiées
Graphes de convergence de la fitness
Arbres d'expression génétique
Comparaisons visuelles fonctions cible vs apprises
Export CSV des résultats

Exemples
Fonction 1D
python main.py -mode "run" -f "x**2 + sin(x)" -xmin -5 -xmax 5

Fonction 2D
python main.py -mode "2d" -f "x**2 + y**2" -xmin -1 -xmax 1 -ymin -1 -ymax 1

Benchmarking
python main.py -mode "iterate" -f "x**3 - 2*x + 1" -iter_field max_depth -iter_min 3 -iter_max 8 -out "benchmark.csv"

Développement
Architecture
AlgoGP : Cœur algorithmique de la GP
ChromosomeGP : Représentation des solutions
DialogueGP : Interface utilisateur
ConfigToolsGP : Gestion centralisée des paramètres

Extension
Pour ajouter de nouvelles fonctions mathématiques, modifier configToolsGP.py :
self.functions = {
    'nouvelle_fonction': lambda x: # implémentation,
    # ...
}


