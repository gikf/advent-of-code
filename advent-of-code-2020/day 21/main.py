# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:19:02 2020
"""
from collections import defaultdict


def main():
    lines = [line.strip() for line in get_file_contents()]
    (foods, ingredient_count, allergen_to_food, ingredient_to_food,
     ingredient_to_possible_allergens) = parse_food(lines)
    ingredients_without_allergens, possible = find_possible_allergens(
        allergen_to_food, ingredient_to_food, ingredient_to_possible_allergens
    )
    occurences = count_occurences(ingredients_without_allergens,
                                  ingredient_count)
    print('Without allergens: ', ingredients_without_allergens)
    print(f'Occurences of ingredients without allergens: {occurences}')
    ingredient_allergen = find_allergens(possible)
    print('Ingredient allergens: ', ingredient_allergen)
    print('Sorted by allergen: ', ','.join(sorted(
        ingredient_allergen, key=lambda ing: ingredient_allergen[ing]
    )))


def find_allergens(ingredients):
    """Return ingredients with cooresponding allergen."""
    by_allergens_count = sorted(ingredients, key=lambda i: len(ingredients[i]))
    for ingredient in by_allergens_count:
        if len(ingredients[ingredient]) == 1:
            for other_ingredient, allergens in ingredients.items():
                if ingredient == other_ingredient:
                    continue
                ingredients[other_ingredient] = (allergens
                                                 - ingredients[ingredient])
    return {
        ingredient: allergen.pop()
        for ingredient, allergen in ingredients.items()
    }


def find_possible_allergens(
        allergen_to_food, ingredient_to_food, ingredient_to_allergens):
    """Return ingredients without allergens and with possible allergens."""
    ingredients_without_allergens = set()
    ingredient_to_possible_allergens = {}
    for ingredient, allergens in ingredient_to_allergens.items():
        possible_allergens = set()
        for allergen in allergens:
            if not allergen_to_food[allergen] - ingredient_to_food[ingredient]:
                possible_allergens.add(allergen)
        if possible_allergens:
            ingredient_to_possible_allergens[ingredient] = possible_allergens
        else:
            ingredients_without_allergens.add(ingredient)
    return ingredients_without_allergens, ingredient_to_possible_allergens


def get_ingredients_with_allergens(
        ingredient_to_food, ingredients_without_allergens):
    """Return ingredients not present in ingredients_without_allergens."""
    return {
        ingredient: food
        for ingredient, food in ingredient_to_food.items()
        if ingredient not in ingredients_without_allergens
    }


def count_occurences(ingredients, ingredient_count):
    """Count number of occurences of ingredients based on ingredient_count."""
    return sum(ingredient_count[ingredient] for ingredient in ingredients)


def parse_food(lines):
    """Parse food from input lines.

    Returns
        foods: list -> dict, list of food dicts, having key for ingredients
        and allergen sets
        ingredient_count: dict ingredinet -> count, ingredient to count how
        many times ingredient occurs in food
        allergen_to_food: dict allergen -> set, allergen to set of foods in
        which allergen occurs
        ingredient_to_food: dict ingredient -> set, ingredinet to set of foods
        in which ingredient occurs
        ingredient_to_possible_allergen: dict ingredient -> set, ingredient
        to set of possible allergens of ingredient
    """
    ingredient_count = defaultdict(int)
    allergen_to_food = defaultdict(set)
    ingredient_to_food = defaultdict(set)
    ingredient_to_possible_allergens = defaultdict(set)
    foods = []
    for index, line in enumerate(lines):
        ingredients, allergens = line.split(' (contains')
        ingredients = ingredients.split()
        allergens = [allergen.strip()
                     for allergen in allergens[:-1].split(', ')]
        foods.append({'ingredients': ingredients,
                      'allergens': allergens})
        for ingredient in ingredients:
            ingredient_count[ingredient] += 1
            ingredient_to_food[ingredient].add(index)
            ingredient_to_possible_allergens[ingredient].update(allergens)
        for allergen in allergens:
            allergen_to_food[allergen].add(index)
    return (foods, ingredient_count, allergen_to_food, ingredient_to_food,
            ingredient_to_possible_allergens)


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
