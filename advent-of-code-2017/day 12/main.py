"""Advent of Code 2017 Day 12."""
from collections import defaultdict, deque


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    pipes = parse_pipes(lines)
    group = get_pipes_group(pipes, 0)
    print(f'Size of group including pipe with ID 0: {len(group)}')
    groups = get_groups(pipes)
    print(f'Number of groups: {len(groups)}')


def get_groups(pipes):
    """Find all separate groups in pipes."""
    seen = set()
    groups = []
    for pipe_id, targets in pipes.items():
        if pipe_id in seen:
            continue
        new_group = get_pipes_group(pipes, pipe_id)
        groups.append(new_group)
        seen = seen | new_group
    return groups


def get_pipes_group(pipes, pipe_id):
    """Starting from pipe_id find all pipes in group containing pipe_id."""
    group = set()
    queue = deque([pipe_id])
    while queue:
        cur_pipe = queue.popleft()
        if cur_pipe in group:
            continue
        group.add(cur_pipe)
        queue.extend(pipes[cur_pipe])
    return group


def parse_pipes(lines):
    """Parse lines to dictionary of pipes IDs mapped to set connected pipes."""
    pipes = defaultdict(set)
    for line in lines:
        source, *targets = [int(pipe_id)
                            for part in line.split(' <-> ')
                            for pipe_id in part.split(', ')]
        pipes[source] = pipes[source] | set(targets)
        for target in targets:
            pipes[target].add(source)
    return pipes


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
