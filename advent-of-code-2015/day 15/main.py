"""Advent of Code 2015 Day 15."""
import math


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    ingredients = parse_ingredients(lines)
    recipes = get_combinations(100, 4, [])
    scores = score_recipes(recipes, ingredients, score_recipe)
    print(f'Best score of recipe: {sorted(scores, reverse=True)[0]}')
    scores_with_500_callories = score_recipes(
        recipes, ingredients, score_with_500_callories
    )
    print('Best score of recipe with calories exact to 500: '
          f'{sorted(scores_with_500_callories, reverse=True)[0]}')


def score_recipes(recipes, ingredients, scorer):
    """Score recipies based on ingredients with scorer function."""
    ingredients_order = [*ingredients]
    return [(scorer(recipe, ingredients),
             recipe,
             ingredients_order)
            for recipe in recipes]


def score_with_500_callories(*args, **kwargs):
    """Call scoring function adding score_of and exact_value requirements."""
    return score_recipe(*args, **kwargs, score_of='calories', exact_value=500)


def score_recipe(recipe, ingredients, score_of=None, exact_value=None):
    """Score recipe using ingredients.

    Optionally property score of score_of can be required to be exact_value.
    """
    if (score_of is not None
            and score_property(score_of, recipe, ingredients) != exact_value):
        return 0
    properties_to_score = {'capacity', 'durability', 'flavor', 'texture'}
    scores = []
    for index, property_name in enumerate(properties_to_score):
        cur_score = score_property(property_name, recipe, ingredients)
        if not cur_score > 0:
            return 0
        scores.append(cur_score)
    return math.prod(scores)


def score_property(property_name, recipe, ingredients):
    """Score property_name according to spoons of ingredients in recipe."""
    score = 0
    for amount, properties in zip(recipe, ingredients.values()):
        value = properties[property_name]
        ingredient_value = amount * value
        score += ingredient_value
    return score


def get_combinations(limit, numbers_count, combination):
    """Get all combinations of numbers_count numbers summing to limit."""
    if sum(combination) >= limit:
        return None
    if numbers_count == 1:
        return [combination + [limit - sum(combination)]]
    combinations = []
    for number in range(1, limit - numbers_count + 2):
        next_combinations = get_combinations(limit,
                                             numbers_count - 1,
                                             combination + [number])
        if next_combinations:
            combinations.extend(next_combinations)
    return combinations


def parse_ingredients(lines):
    """Parse lines to dictionary of ingredients."""
    return dict(parse_ingredient(line) for line in lines)


def parse_ingredient(line):
    """Parse line to tuple with name and dict of properties of ingredient."""
    name, rest = line.split(': ')
    properties = {}
    for part in rest.split(', '):
        property_name, value = part.split()
        properties[property_name] = int(value)
    return name, properties


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
