"""Advent of Code 2019 Day 1."""


def main(file_input='input.txt'):
    masses = [int(num.strip()) for num in get_file_contents(file_input)]
    needed_fuel = get_needed_fuel(masses, module_fuel)
    print(f'Fuel requirement: {needed_fuel}')
    needed_fuel_with_fuel_mass = get_needed_fuel(masses, module_fuel_with_fuel)
    print('Fuel requirement, including mass of the added fuel '
          f'{needed_fuel_with_fuel_mass}')


def get_needed_fuel(masses, fuel_calculator):
    """Get needed fuel for masses using fuel_calculator function."""
    return sum(fuel_calculator(mass) for mass in masses)


def module_fuel(mass):
    """Calculate needed fuel for mass."""
    return mass // 3 - 2


def module_fuel_with_fuel(mass):
    """Calculate needed fuel for mass, including fuel mass."""
    total_fuel = 0
    while mass > 0:
        mass = module_fuel(mass)
        total_fuel += mass if mass > 0 else 0
    return total_fuel


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
