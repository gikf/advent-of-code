"""Advent of Code 2018 Day 14."""


puzzle = 633601


def main(puzzle=puzzle):
    recipes = [3, 7]
    elves = [0, 1]
    runs = (
        ('Score of 10 recipes after the puzzle recipes', ten_recipes_condition,
         ten_recipes_result),
        ('Recipes on the left of the puzzle sequence', first_score_condition,
         first_score_result)
    )
    for description, condition_func, result_func in runs:
        result = find_recipes(
                    recipes[:], elves[:], puzzle, condition_func, result_func)
        print(f'{description}: {result}')


def find_recipes(recipes, cur_recipes, puzzle, condition, result):
    """Find recipes as long as condition function is True.

    Returns result of result function, based on recipes and puzzle.
    """
    while condition(recipes, puzzle):
        next_recipe = sum(recipes[recipe] for recipe in cur_recipes)
        digits = next_recipe_digits(next_recipe)
        recipes.extend(digits)
        cur_recipes = [(recipe + 1 + recipes[recipe]) % len(recipes)
                       for recipe in cur_recipes]
    return result(recipes, puzzle)


def first_score_condition(recipes, puzzle):
    """Check if puzzle is present at the end of recipes."""
    length, wanted = get_puzzle_data(puzzle)
    return (not compare(recipes[-length:], wanted)
            and not compare(recipes[-length - 1: -1], wanted))


def compare(recipe, wanted):
    """Compare recipe against wanted."""
    for num1, num2 in zip(wanted, recipe):
        if num1 != num2:
            return False
    return True


def first_score_result(recipes, puzzle):
    """Return number of recipes on the left of the first puzzle occurrence."""
    length, wanted = get_puzzle_data(puzzle)
    if wanted == recipes[-length:]:
        return len(recipes) - length
    return len(recipes) - length - 1


def get_puzzle_data(puzzle, data={}):
    """Get length and list of numbers from puzzle."""
    if not data:
        data['length'] = len(str(puzzle))
        data['wanted'] = [int(num) for num in str(puzzle)]
    return data['length'], data['wanted']


def ten_recipes_condition(recipes, puzzle):
    """Check if number of recipes passed needed puzzle number."""
    return len(recipes) < puzzle + 10


def ten_recipes_result(recipes, puzzle):
    """Return 10 recipes after the recipe number puzzle."""
    return ''.join(str(num) for num in recipes[puzzle:puzzle + 10])


def next_recipe_digits(cur_recipe):
    """Calculate next recipe, based on the cur_recipe."""
    if cur_recipe == 0:
        return [0]
    digits = []
    while cur_recipe > 0:
        digits.append(cur_recipe % 10)
        cur_recipe = cur_recipe // 10
    return digits[::-1]


if __name__ == '__main__':
    main()
