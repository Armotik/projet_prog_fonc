from dataclasses import dataclass
from typing import List

@dataclass
class Ingredient:
    name: str
    amount: float
    unit: str = None

@dataclass
class Step:
    description: str

@dataclass
class Preparation:
    steps: List[Step]

@dataclass
class Nutrition:
    calories: int
    fat: str
    carbohydrates: str
    protein: str

@dataclass
class Related:
    ref: str
    description: str

@dataclass
class Recipe:
    id: str
    title: str
    date: str
    ingredients: List[Ingredient]
    preparation: Preparation
    comment: str
    nutrition: Nutrition
    related: Related