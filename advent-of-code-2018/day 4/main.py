"""Advent of Code 2018 Day 4."""
from collections import defaultdict
import re


def main(file_input='input.txt'):
    lines = sorted([line.strip() for line in get_file_contents(file_input)])
    guard_to_sleeps = parse_guards(lines)
    sleepy_guard_id = max(guard_to_sleeps.items(), key=total_sleep_minutes)[0]
    guard_to_most_asleep_minute = get_most_alseep_minutes(guard_to_sleeps)
    sleepy_guard_most_asleep_minute = (
        guard_to_most_asleep_minute[sleepy_guard_id][1])
    print('ID of guard with most minutes asleep multiplied by minute '
          'which that guard spend asleep the most: ',
          (sleepy_guard_id * sleepy_guard_most_asleep_minute))
    guard_with_most_asleep_minute = max(
        guard_to_most_asleep_minute, key=guard_to_most_asleep_minute.get)
    most_asleep_minute = (
        guard_to_most_asleep_minute[guard_with_most_asleep_minute])
    print('ID of guard with most asleep minute multiplied by that minute: ',
          guard_with_most_asleep_minute * most_asleep_minute[1])


def get_most_alseep_minutes(guards):
    """Get dictionary of guards to most asleep minute."""
    guard_to_most_asleep_minute = {}
    for guard, shifts in guards.items():
        guard_to_most_asleep_minute[guard] = find_most_asleep_minute(shifts)
    return guard_to_most_asleep_minute


def find_most_asleep_minute(shifts):
    """Find minute during which guard was most often asleep."""
    minutes = defaultdict(int)
    for shift in shifts:
        sleep, wakes = shift
        for minute in range(sleep, wakes):
            minutes[minute] += 1
    max_minute = max(minutes, key=minutes.get)
    return minutes[max_minute], max_minute


def total_sleep_minutes(guard):
    """Calculate total minutes slept by guard."""
    _, shifts = guard
    return sum(
        wakes - sleeps
        for sleeps, wakes in shifts
    )


def get_minutes(line):
    """Get minutes from line."""
    regex = r':(\d{2})]'
    return re.search(regex, line).group(1)


def get_guard_id(line):
    """Get guard ID from line."""
    regex = r'#(\d+)'
    return re.search(regex, line).group(1)


def parse_guards(lines):
    """Parse lines to dictionary of guards to list of sleeps."""
    guards = defaultdict(list)
    for line in lines:
        minutes = int(get_minutes(line))
        if 'Guard' in line:
            cur_guard = int(get_guard_id(line))
        elif 'asleep' in line:
            sleep = minutes
        elif 'wakes' in line:
            wakes = minutes
            guards[cur_guard].append((sleep, wakes))
    return guards


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
