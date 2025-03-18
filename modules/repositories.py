import xml.etree.ElementTree as ET
from typing import List

from modules.models import Recipe, Step, Ingredient, Preparation, Nutrition, Related
from functools import reduce
from collections import Counter, defaultdict


def _init_recipes(data, namespace=None) -> List[Recipe]:
    """
    Display : Initialisation des recettes

    Description : Écrire une fonction init_recipes() qui analyse le fichier XML et charge les données sous forme de liste immuable de recettes
    :param data: le chemin du fichier XML
    :param namespace: le namespace utilisé dans le fichier XML
    :type data: str
    :type namespace: dict
    :return: une liste immuable de recettes
    """
    if namespace is None:
        namespace = {"rcp": "http://www.brics.dk/ixwt/recipes"}
    tree = ET.parse(data)
    root = tree.getroot()

    recipes = root.findall(".//rcp:recipe", namespaces=namespace)

    extract_text = lambda elem, tag: elem.find(tag, namespaces=namespace).text if elem.find(tag,
                                                                                            namespaces=namespace) is not None else ""

    extract_ingredients = lambda recipe: list(map(lambda ing: Ingredient(
        name=ing.get("name"),
        amount=float(ing.get("amount", 0)) if ing.get("amount") and ing.get("amount") != "*" else 0,
        unit=ing.get("unit", "")
    ), recipe.findall(".//rcp:ingredient", namespaces=namespace)))

    extract_steps = lambda recipe: Preparation(
        steps=list(map(lambda step: Step(step.text), recipe.findall(".//rcp:step", namespaces=namespace))))

    extract_nutrition = lambda recipe: Nutrition(
        calories=int(recipe.find(".//rcp:nutrition", namespaces=namespace).get("calories")),
        fat=recipe.find(".//rcp:nutrition", namespaces=namespace).get("fat"),
        carbohydrates=recipe.find(".//rcp:nutrition", namespaces=namespace).get("carbohydrates"),
        protein=recipe.find(".//rcp:nutrition", namespaces=namespace).get("protein")
    )

    extract_related = lambda recipe: Related(
        ref=recipe.find(".//rcp:related", namespaces=namespace).get("ref") if recipe.find(".//rcp:related",
                                                                                          namespaces=namespace) is not None else "",
        description=extract_text(recipe, ".//rcp:related")
    )

    return list(map(lambda recipe: Recipe(
        id=recipe.get("id"),
        title=recipe.find(".//rcp:title", namespaces=namespace).text,
        date=recipe.find(".//rcp:date", namespaces=namespace).text,
        ingredients=extract_ingredients(recipe),
        preparation=extract_steps(recipe),
        comment=extract_text(recipe, ".//rcp:comment"),
        nutrition=extract_nutrition(recipe),
        related=extract_related(recipe)
    ), recipes))


class RecipeRepository:

    def __init__(self, data='../data/recipes.xml'):
        """
        Display : Initialisation du Repository

        Description : Initialisation du Repository avec les données du fichier XML

        :param data: le chemin du fichier XML
        :type data: str
        """
        self.recipes = _init_recipes(data=data)

    def get_recipes(self) -> List[Recipe]:
        """
        Display : Récupération des recettes

        Description : Fonction qui retourne la liste des recettes

        :return:  La liste des recettes
        """
        return self.recipes

    def get_ingredients(self) -> List[Ingredient]:
        """
        Display : Récupération des ingrédients

        Description : Fonction qui retourne la liste des ingrédients
        :return:  La liste des ingrédients
        """
        return reduce(lambda acc, r: acc + r.ingredients, self.recipes, [])

    def list_titles(self) -> List[str]:
        """
        Display : Liste des titres des recettes

        Description : Écrire une fonction qui retourne la liste des titres des recettes en utilisant map().
        :return: Une liste des titres des recettes
        """
        return list(map(lambda recipe: recipe.title, self.recipes))

    def calculate_eggs(self) -> int:
        """
        Display : Total Œufs

        Description : Écrire une fonction qui calcule le nombre total d’œufs utilisés dans toutes les recettes en utilisant map() et reduce()
        :return: Le nombre total d’œufs utilisés dans toutes les recettes
        """
        return reduce(
            lambda acc, amount: acc + amount,
            map(lambda ing: ing.amount,
                filter(lambda ing: "egg" in ing.name.lower(),
                       reduce(lambda acc, r: acc + r.ingredients, self.recipes, []))
                ),
            0
        )

    def olive_oil_recipes(self) -> List[Recipe]:
        """
        Display : Recettes à l'huile d'olive

        Description : Écrire une fonction qui filtre et retourne les recettes utilisant de l’huile d’olive avec filter()
        :return: Une liste des recettes utilisant de l’huile d’olive
        """
        return list(filter(lambda recipe: any(map(lambda ing: "olive oil" in ing.name.lower(), recipe.ingredients)),
                           self.recipes))

    def egg_by_recipe(self) -> dict:
        """
        Display : Œufs par recette

        Description : Écrire une fonction qui retourne un dictionnaire contenant le nombre d’œufs par recette en utilisant map().

        Graph State : bar : (x: Recette, y: eggs)
        :return: Un dictionnaire contenant le nombre d’œufs par recette
        """
        return dict(
            map(
                lambda recipe: (recipe.title, reduce(
                    lambda acc, ing: acc + ing.amount,
                    filter(lambda ing: "egg" in ing.name.lower(), recipe.ingredients),
                    0
                )),
                self.recipes
            )
        )

    def less_than_500cal(self) -> List[Recipe]:
        """
        Display : Recettes moins de 500 cal

        Description : Écrire une fonction qui retourne les recettes fournissant moins de 500 calories en utilisant filter().

        Graph State : bar : (x: Recette, y: calories)
        :return: Les recettes ayant moins de 500 cal
        """
        return list(filter(lambda recipe: recipe.nutrition.calories < 500, self.recipes))

    def sugar_quantity(self, recipe="Zuppa Inglese"):
        """
        Display : Quantité de sucre dans "Zuppa Inglese"

        Description : Écrire une fonction qui retourne la quantité de sucre utilisée par la recette "Zuppa Inglese".

        :param recipe: Le titre de la recette
        :type recipe: str
        :return: La quantité de sucre utilisée par la recette
        """
        return reduce(
            lambda acc, ing: acc + ing.amount,
            filter(lambda ing: "sugar" in ing.name.lower(),
                   next(filter(lambda r: r.title == recipe, self.recipes)).ingredients),
            0
        )

    def first_2_steps(self, recipe="Zuppa Inglese") -> List[Step]:
        """
        Display : Deux premières étapes "Zuppa Inglese"

        Description : Écrire une fonction qui retourne les deux premières étapes de la recette "Zuppa Inglese".

        :param recipe: Le titre de la recette
        :type recipe: str
        :return: Les deux premières étapes de la recette
        """
        return next(filter(lambda r: r.title == recipe, self.recipes)).preparation.steps[:2]

    def more_than_5_steps(self) -> List[Recipe]:
        """
        Display : Recettes plus de 5 étapes

        Description : Écrire une fonction qui retourne les recettes nécessitant plus de 5 étapes en utilisant filter()

        Graph State : bar : (x: Recette, y: steps)
        :return: Les recettes ayant plus de 5 étapes
        """
        return list(filter(lambda recipe: len(recipe.preparation.steps) > 5, self.recipes))

    def butter_free(self) -> List[Recipe]:
        """
        Display : Recettes sans beurre

        Description : Écrire une fonction qui retourne les recettes ne contenant pas de beurre en utilisant filter()

        :return: Les recettes ne contenant pas de beurre
        """
        return list(filter(lambda recipe: not any(map(lambda ing: "butter" in ing.name.lower(), recipe.ingredients)),
                           self.recipes))

    def common_ingredients(self, comparator="Zuppa Inglese") -> List[Recipe]:
        """
        Display : Ingrédients en commun avec "Zuppa Inglese"

        Description : Écrire une fonction qui retourne les recettes ayant des ingrédients en commun avec la recette "Zuppa Inglese" en utilisant filter() et set()

        Graph State : bar : (x: Recette, y: ingredients)
        :param comparator: Le titre de la recette à comparer avec les autres recettes
        :type comparator: str
        :return: Les recettes ayant des ingrédients en commun avec la recette "Zuppa Inglese"
        """
        return list(filter(lambda recipe: set(map(lambda ing: ing.name.lower(), recipe.ingredients)).intersection(
            map(lambda ing: ing.name.lower(), next(filter(lambda r: r.title == comparator, self.recipes)).ingredients)
        ), self.recipes))

    def most_caloric(self) -> Recipe:
        """
        Display : Recette la plus calorique

        Description : Écrire une fonction qui retourne la recette la plus calorique en utilisant max()
        :return: La recette la plus calorique
        """
        return max(self.recipes, key=lambda recipe: recipe.nutrition.calories)

    def most_common_unit(self) -> str:
        """
        Display : Unité de mesure la plus fréquente

        Description : Écrire une fonction qui retourne l’unité de mesure la plus fréquente dans les ingrédients en utilisant Counter().
        :return: L’unité de mesure la plus fréquente dans les ingrédients
        """
        units = Counter(filter(lambda unit: unit,
                               map(lambda ing: ing.unit, reduce(lambda acc, r: acc + r.ingredients, self.recipes, []))))
        return units.most_common(1)[0][0]

    def ingredients_count_by_recipe(self) -> dict:
        """
        Display : Nombre d'ingrédients par recette

        Description : Écrire une fonction qui retourne un dictionnaire contenant le nombre d’ingrédients par recette en utilisant map().

        Graph State : bar : (x: Recette, y: ingredients)
        :return: Un dictionnaire contenant le nombre d’ingrédients par recette
        """
        return dict(
            map(
                lambda recipe: (recipe.title, len(recipe.ingredients)),
                self.recipes
            )
        )

    def fattest_recipe(self) -> Recipe:
        """
        Display : Recette la plus grasse

        Description : Écrire une fonction qui retourne la recette la plus grasse en utilisant max()
        :return: La recette la plus grasse
        """
        return max(self.recipes, key=lambda recipe: float(recipe.nutrition.fat.replace("%", "")))

    def most_common_ingredient(self) -> str:
        """
        Display : Ingrédient le plus fréquent

        Description : Écrire une fonction qui retourne l’ingrédient le plus fréquent en utilisant Counter().
        :return: L’ingrédient le plus fréquent
        """
        ingredients = Counter(map(lambda ing: ing.name, reduce(lambda acc, r: acc + r.ingredients, self.recipes, [])))
        return ingredients.most_common(1)[0][0]

    def sorted_by_ingredients(self) -> List[Recipe]:
        """
        Display : Trie par nombre d'ingrédients

        Description : Écrire une fonction qui affiche les recettes triées par nombre d’ingrédients en utilisant sorted()

        Graph State : bar : (x: Recette, y: ingredients)
        :return: Les recettes triées par nombre d’ingrédients
        """
        return sorted(self.recipes, key=lambda recipe: len(recipe.ingredients))

    def recipes_by_ingredients(self) -> defaultdict:
        """
        Display : Recettes par ingrédient

        Description : Écrire une fonction qui affiche pour chaque ingrédient la liste des recettes qui l’utilisent en utilisant defaultdict()
        :return: Un dictionnaire contenant la liste des noms recettes pour chaque ingrédient
        """
        return defaultdict(list, dict(
            map(
                lambda ing: (ing, list(map(lambda recipe: recipe.title,
                                           filter(lambda recipe: any(map(lambda i: i.name == ing, recipe.ingredients)),
                                                  self.recipes))),
                             ),
                set(map(lambda ing: ing.name, reduce(lambda acc, r: acc + r.ingredients, self.recipes, [])))
            )
        ))

    def recipes_by_number_of_step(self) -> defaultdict:
        """
        Display : Recettes par nombre d'étapes

        Description : Écrire une fonction qui calcule la répartition des recettes en fonction du nombre d’étapes.
        :return: Un dictionnaire contenant le nombre de recettes par nombre d’étapes
        """
        return defaultdict(int, dict(map(lambda recipe: (len(recipe.preparation.steps), 1), self.recipes)))

    def easiest_recipe(self) -> Recipe:
        """
        Display : Recette la plus simple

        Description : Écrire une fonction qui retourne la recette la plus facile (avec le moins d’étapes) en utilisant min()
        :return: La recette la plus simple
        """
        return min(self.recipes, key=lambda recipe: len(recipe.preparation.steps))
