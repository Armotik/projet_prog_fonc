import matplotlib.pyplot as plt
import streamlit as st
from modules.repositories import RecipeRepository
import inspect
import re


def _get_display_names(cls):
    """
    Retourne un dictionnaire des noms d'affichage des méthodes d'une classe
    :param cls: Classe à inspecter
    :return: Dictionnaire des noms d'affichage
    """
    methods = inspect.getmembers(cls, predicate=inspect.isfunction) # Récupère les méthodes de la classe
    docstrings = map(lambda method: (method[0], inspect.getdoc(method[1])), methods) # Récupère les docstrings des méthodes
    display_lines = filter(lambda doc: doc[1] and any("Display :" in line for line in doc[1].split('\n')), docstrings) # Filtre les docstrings contenant "Display :"
    display_names = dict(map(lambda doc: (
        doc[0], next(line.split(":", 1)[1].strip() for line in doc[1].split('\n') if "Display :" in line)),
                             display_lines)) # Récupère les noms d'affichage des méthodes
    return display_names


def _get_description(func):
    """
    Retourne la description d'une fonction
    :param func: Fonction à inspecter
    :return: Description de la fonction
    """
    return inspect.getdoc(func)


def _get_graph_state(func):
    """
    Retourne si une fonction affiche un graphique et les paramètres de ce graphique
    :param func: Fonction à inspecter
    :return: [bool, str, str, str] : [True si la fonction affiche un graphique, Type de graphique, Nom de l'axe x, Nom de l'axe y]
    """
    doc = inspect.getdoc(func) # Récupère la docstring de la fonction
    if not doc:
        return [False, None, None, None]

    lines = doc.split("\n")
    graph_line = next(filter(lambda line: "Graph State :" in line, lines), None) # Récupère la ligne contenant "Graph State :"
    if not graph_line:
        return [False, None, None, None]

    # Pattern : Graph State : str : (x: str, y: str)
    pattern = r"Graph State\s*:\s*(\w+)\s*:\s*\(x:\s*(\w+),\s*y:\s*(\w+)\)"
    match = re.match(pattern, graph_line) # Récupère les paramètres du graphique

    if match:
        return [True, match.group(1), match.group(2), match.group(3)]

    return None


repo = RecipeRepository(data="./data/recipes.xml")

all_recipes = repo.get_recipes()
all_ingredients = repo.get_ingredients()

display_names = _get_display_names(RecipeRepository)
menu_options = ["Menu principal"] + list(display_names.values())
menu_options.pop(1) # Supprime la méthode "_init_recipes" du menu

st.title("Projet - Programmation Fonctionnelle")

menu = st.sidebar.radio("Menu", menu_options, index=0)
presentation_mode = st.sidebar.radio("Mode de présentation", ["Textuel", "Graphique"])

if menu == "Menu principal":
    st.write("Bienvenue dans le menu principal, veuillez choisir une méthode à tester.")
    st.write("Les méthodes disponibles sont :")
    st.write(list(display_names.values()))

else:
    method_name = next(name for name, display_name in display_names.items() if display_name == menu)
    method = getattr(repo, method_name)
    result = method()

    if presentation_mode == "Textuel":

        st.write("## Méthode : ", menu)
        st.write("### Description :")
        st.write(_get_description(method))

        st.write("### Résultat :")

        st.write(result)

    else:
        graph_state = _get_graph_state(method)
        if graph_state and graph_state[0]:

            st.write("### Graphique :")
            if graph_state[1] == "bar":
                x = [recipe.title for recipe in result] if graph_state[2] == "Recette" and type(result) != dict else result.keys()

                if graph_state[3] == "calories":

                    y = [getattr(recipe.nutrition, graph_state[3]) for recipe in result]

                elif graph_state[3] == "steps":
                    y = [len(getattr(recipe.preparation, graph_state[3])) for recipe in result]

                elif graph_state[3] in list(map(lambda x: x.name, all_ingredients)) or graph_state[3] == "ingredients":

                    y = result.values() if type(result) == dict else [len(getattr(recipe, graph_state[3])) for recipe in result if hasattr(recipe, graph_state[3])]

                else:
                    y = [getattr(recipe, graph_state[3]) for recipe in result]

                y = [item if isinstance(item, (int, float)) else len(item) for item in y]

                fig = plt.figure(figsize=(10, 5))
                plt.bar(x, y)
                plt.xlabel(graph_state[2])
                plt.ylabel(graph_state[3])
                plt.title(f"Nombre de {graph_state[3]} par {graph_state[2]}")

                st.pyplot(fig)
            else:
                st.write("Type de graphique non reconnu.")
        else:

            st.write("### Graphique :")
            st.write("Pas de graphique à afficher pour cette méthode.")
