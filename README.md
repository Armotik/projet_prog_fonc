# Programmation Fonctionnelle - Projet

## Objectif

Le but de ce projet est de développer une application en Python qui manipule les
informations provenant d’un fichier XML contenant des recettes, en adoptant un
raisonnement fonctionnel à l’aide des fonctions map, filter et reduce

## Description

Le fichier recipes.xml décrit un ensemble de recettes. L'objectif est d'effectuer des
traitements sur ces données de manière efficace en exploitant la programmation
fonctionnelle.

## Structure du projet

Le projet est structuré de la manière suivante :

```bash
.
├── data
│   └── recipes.xml
├── modules
│   ├── __init__.py
│   ├── models.py
│   └── repositories.py
├── .gitignore
├── presentation.py
├── requirements.txt
└── README.md

```

- Le fichier [recipes.xml](data/recipes.xml) contient les données des recettes.
- Le module [models.py](modules/models.py) contient les classes qui représentent les données des recettes.
- Le module [repositories.py](modules/repositories.py) contient les fonctions qui permettent de lire les données du
  fichier XML.
- Le fichier [presentation.py](presentation.py) contient le code de l'interface utilisateur.
- Le fichier [requirements.txt](requirements.txt) contient la liste des dépendances du projet.
- Le fichier [README.md](README.md) contient la documentation du projet.

## Installation

Pour installer les dépendances du projet, exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

Comme l'application utilise [Streamlit](https://streamlit.io/) pour l'interface utilisateur, vous devez lancer
l'application en exécutant la
commande suivante dans le terminal au niveau du répertoire du projet :

```bash
streamlit run presentation.py
```

## modules

### models.py

Ce module contient les classes qui représentent les données des recettes.

Ces classes sont les suivantes :

- `Ingredient(name: str, amount, float, unit: str)` : représente un ingrédient d'une recette.
- `Step(description: str)` : représente une étape d'une recette.
- `Preparation(steps: List[Step])` : représente les étapes de préparation d'une recette.
- `Nutrition(calories: int, fat: str, carbohydrates: str, protein: str)` : représente les informations nutritionnelles
  d'une recette.
- `Related(ref: str, description: str)` : représente les recettes connexes.
- `Recipe(id: str, title: str, date: str, ingredients: List[Ingredient], preparation: Preparation, comment: str,
  nutrition: Nutrition, related: Related)` : représente une recette en utilisant les classes précédentes.

**Bibliothèques utilisées :**

- [dataclasses](https://docs.python.org/3/library/dataclasses.html) : pour créer des classes de données.
- [typing](https://docs.python.org/3/library/typing.html): pour définir les Listes.

### repositories.py

Ce module contient les fonctions qui permettent de lire les données du fichier XML.

Toutes les fonctions possèdent une [Docstring](https://peps.python.org/pep-0257/) structurée de la manière suivante :

```python
def function_name(arguments) -> return_type:
    """
    Display : Nom de la fonction (Utilisé pour l'affichage)
    
    Description : Description de la fonction.
    
    Graph State : graph_type : (x: param_name, y: param_name) (Si le résultat de la fonction peut être affiché sous forme de graphique)

    :param arguments: Description des arguments. (Si la fonction ne prend pas d'arguments, ne pas spécifier cette section)
    :type arguments: Type des arguments. (Si la fonction ne prend pas d'arguments, ne pas spécifier cette section)
    :return: Description de la valeur de retour. (Si la fonction ne retourne rien, ne pas spécifier cette section)
    """
```

__Les fonctions sont les suivantes :__

- `_init_recipes(data, namespace=None)` : initialise les recettes à partir du fichier XML et retourne une liste de
  recettes (List[Recipe]).
- `get_recipes()` : retourne la liste des recettes.
- `list_titles()` : retourne la liste des titres des recettes.
- `calculate_eggs()` : retourne le nombre total d'œufs utilisés dans les recettes.
- `olive_oil_recipes()` : retourne la liste des recettes qui contiennent de l'huile d'olive.
- `egg_by_recipe()` : retourne un dictionnaire contenant le nombre d’œufs par recette
- `less_than_500cal()` : retourne la liste des recettes qui contiennent moins de 500 calories.
- `sugar_quantity(recipe="Zuppa Inglese")` : retourne la quantité de sucre utilisée dans une recette donnée (par
  défaut "Zuppa Inglese").
- `first_2_steps(recipe="Zuppa Inglese")` : retourne les deux premières étapes de préparation d'une recette donnée (par
  défaut "Zuppa Inglese").
- `more_than_5_steps()` : retourne la liste des recettes qui contiennent plus de 5 étapes de préparation.
- `butter_free()` : retourne la liste des recettes qui ne contiennent pas de beurre.
- `common_ingredients(comparator="Zuppa Inglese")` : retourne Les recettes ayant des ingrédients en commun avec une
  recette donnée (par défaut "Zuppa Inglese").
- `most_caloric()` : retourne la recette la plus calorique.
- `most_common_unit()` : retourne l'unité la plus utilisée dans les ingrédients.
- `ingredients_count_by_recipe()` : retourne un dictionnaire contenant le nombre d'ingrédients par recette.
- `fattest_recipe()` : retourne la recette la plus grasse.
- `most_common_ingredient()` : retourne l'ingrédient le plus utilisé.
- `sorted_by_ingredients()` : retourne la liste des recettes triées par nombre d'ingrédients.
- `recipes_by_ingredients()` : retourne un dictionnaire contenant la liste des noms recettes pour chaque ingrédient
- `recipes_by_number_of_step()` : retourne un dictionnaire contenant la liste des noms recettes pour chaque nombre
  d'étapes
- `easiest_recipe()` : retourne la recette la plus facile, c'est-à-dire celle qui contient le moins d'étapes de
  préparation.

**Bibliothèques utilisées :**

- [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) : pour lire les données du
  fichier XML.
- [typing](https://docs.python.org/3/library/typing.html) : pour définir les Listes et les Dictionnaires.
- [collections](https://docs.python.org/3/library/collections.html) : pour utiliser les `Counter` et les `defaultdict`.
- [functools](https://docs.python.org/3/library/functools.html) : pour utiliser les `reduce`.
- [models](modules/repositories.py) : pour utiliser les classes du module [models.py](modules/models.py).

### presentation.py

Ce fichier contient le code de l'interface utilisateur.

L'interface utilisateur est développée en utilisant [Streamlit](https://streamlit.io/).

Le fichier possède des fonctions privées qui permettent de récupérer les informations nécessaires pour l'affichage des
résultats.

- `_get_display_name(cls)` : retourne le nom d'affichage d'une classe.
- `_get_description(func)` : retourne la description d'une fonction.
- `_get_graph_state(func)` : retourne le type de graphique d'une fonction.

1. L'utilisateur peut choisir d'afficher les résultats sous forme de graphique ou de texte dans un menu à gauche.
2. L'utilisateur peut choisir une fonction à exécuter dans un menu à gauche.

**Bibliothèques utilisées :**

- [streamlit](https://streamlit.io/) : pour créer l'interface utilisateur.
- [matplotlib](https://matplotlib.org/) : pour afficher les graphiques avec `pyplot` et `Streamlit`.
- [repositories](modules/repositories.py) : pour utiliser les fonctions du
  module [repositories.py](modules/repositories.py).
- [inspect](https://docs.python.org/3/library/inspect.html) : pour inspecter les fonctions.
- [re](https://docs.python.org/3/library/re.html) : pour utiliser les expressions régulières.

## Difficultés rencontrées

- La manipulation des données du fichier XML :
    - Choisir la bonne méthode pour structurer les données.
    - Comment lire les données du fichier XML.
- Certaines fonctions à faire :
    - `recipes_by_ingredients()`
- La création de l'interface utilisateur avec Streamlit.
    - Comment afficher les résultats sous forme de graphique ou de texte, avec la documentation, j'ai réussi à faire
      cela
      mais le plus dur a été de savoir comment généraliser l'affichage des graphiques pour toutes les fonctions. En
      cherchant j'ai décidé d'utiliser la documentation des fonctions pour savoir si le résultat peut être affiché sous
      forme de graphique ou non.

## Améliorations possibles

- Ajouter des tests unitaires pour les fonctions.
- Comme certaines fonctions ne peuvent pas avoir de graphique, j'ai pensé à ajouter un graphique de comparaison entre le
  temps d'execution de la fonction en mode fonctionnel et en mode itératif. Mais je n'ai pas eu le temps et
  j'aurais dû revoir la structure de mon code pour pouvoir le faire.
- Trouver de meilleurs graphiques et les styliser.

## Auteur

- Anthony MUDET

---

## Ressources

- [Streamlit](https://streamlit.io/)
- [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [typing](https://docs.python.org/3/library/typing.html)
- [collections](https://docs.python.org/3/library/collections.html)
- [functools](https://docs.python.org/3/library/functools.html)
- [matplotlib](https://matplotlib.org/)
- [inspect](https://docs.python.org/3/library/inspect.html)
- [re](https://docs.python.org/3/library/re.html)

---

Le projet est disponible sur [GitHub](https://github.com/Armotik/projet_prog_fonc)

---

- Programmation Fonctionnelle - Projet
- Anthony MUDET
- Licence 3 Informatique - La Rochelle Université
- 2025