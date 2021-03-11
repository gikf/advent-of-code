"""Advent of Code 2017 Day 24."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    components = parse_components(lines)
    possible_bridges = bridges(components, set(), [(0, 0)])
    bridges_by_strength = sorted(score_bridges(possible_bridges))
    strongest_bridge = bridges_by_strength[-1]
    print(f'Strength of strongest bridge: {strongest_bridge[0]}')
    bridges_by_length = sorted(
        bridges_by_strength, key=lambda item: len(item[1]))
    strongest_longest_bridge = bridges_by_length[-1]
    print('Strength of strongest bridge from the longest: '
          f'{strongest_longest_bridge[0]}')


def score_bridges(bridges):
    """Score bridges, add score to tuple with bridge."""
    return [(score_bridge(bridge), bridge) for bridge in bridges]


def score_bridge(bridge):
    """Score bridge by adding ports in all components."""
    return sum(sum(component) for component in bridge)


def bridges(components, used, bridge):
    """Get possible bridges from components."""
    if bridge[-1][1] not in components:
        return [bridge]
    input_port = bridge[-1][1]
    if all(component in used for component in components[input_port]):
        return [bridge]
    possible_bridges = []
    for component in components[input_port]:
        if component in used:
            continue
        output_port = get_output_port(component, input_port)
        possible_bridges.extend(
            bridges(components,
                    used | {component},
                    bridge + [(input_port, output_port)]))
    return possible_bridges


def get_output_port(component, input_port):
    """Get output port of the component."""
    if component[0] == component[1]:
        return input_port
    return [port for port in component if port != input_port][0]


def parse_components(lines):
    """Parse lines to components dictionary with port -> component mapping."""
    components = defaultdict(list)
    for line in lines:
        component = tuple([int(num) for num in line.split('/')])
        for port in component:
            components[port].append(component)
    return components


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
