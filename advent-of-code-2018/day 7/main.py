"""Advent of Code 2018 Day 7."""
from collections import defaultdict


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    steps, step_to_prerequisites = parse_steps(lines)
    steps_order = find_steps_order(steps, step_to_prerequisites)
    print(f'Order in which steps can be completed: {steps_order}')
    time_to_complete = find_steps_time(*parse_steps(lines))
    print(f'Time to complete steps with 5 workers: {time_to_complete}')


def find_steps_time(steps, step_to_prerequisites):
    """Find time needed to complete steps."""
    timer = 0
    workers = [[0, ''] for _ in range(5)]
    base_step_time = 60
    step_time_adjust = ord('A')
    while steps or any(worker[0] != 0 for worker in workers):
        for index, worker in enumerate(workers):
            to_complete, cur_step = worker
            if to_complete > 0:
                workers[index][0] -= 1
                continue
            steps = steps - {cur_step}
            update_prerequisities(step_to_prerequisites, cur_step)
            open_steps = get_open_steps(steps, step_to_prerequisites)
            if not open_steps:
                workers[index][1] = ''
                continue
            next_step = open_steps.pop(0)
            steps = steps - {next_step}
            to_complete = base_step_time + ord(next_step) - step_time_adjust
            workers[index] = [to_complete, next_step]
        timer += 1
    return timer - 1


def find_steps_order(steps, step_to_prerequisites):
    """Find steps order in which instructions can be completed."""
    order = []
    cur_step = ''
    while len(steps) > 1:
        steps = steps - {cur_step}
        update_prerequisities(step_to_prerequisites, cur_step)
        cur_step = get_open_steps(steps, step_to_prerequisites)[0]
        order.append(cur_step)
    return ''.join(order)


def update_prerequisities(step_to_prerequisites, cur_step):
    """Update prerequisites to remove cur_step where applicable."""
    for step, prerequisites in step_to_prerequisites.items():
        try:
            step_to_prerequisites[step].remove(cur_step)
        except KeyError:
            pass
    return step


def get_open_steps(steps, prerequisities):
    """Get steps which can be started."""
    return sorted([
        step for step in steps
        if step not in prerequisities or len(prerequisities[step]) == 0])


def parse_steps(lines):
    """Parse lines to set of steps and dict with step to prerequisite."""
    steps = set()
    step_to_prerequisites = defaultdict(set)
    for line in lines:
        split = line.split()
        step, prerequisite = [split[index] for index in (1, -3)]

        steps.add(step)
        steps.add(prerequisite)
        step_to_prerequisites[prerequisite].add(step)
    return steps, step_to_prerequisites


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
