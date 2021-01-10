"""Advent of Code 2015 Day 14."""
from collections import defaultdict


TIME_LIMIT = 2503


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    reindeers = parse_reindeers(lines)
    distances = sorted(fly_for(TIME_LIMIT, reindeers), reverse=True,
                       key=lambda item: item[1])
    print(f'Winner based on distance: {distances[0]}')
    scores = sorted(score_by_leader(TIME_LIMIT, reindeers).items(),
                    reverse=True,
                    key=lambda item: item[1])
    print(f'Winner based on receiving points for leading: {scores[0]}')


def score_by_leader(time_limit, reindeers):
    """Score reeinders race for time_limit, based on current leader."""
    points = defaultdict(int)
    distances = defaultdict(int)
    reindeer_timers = {
        reindeer: {'duration': duration, 'rest': -1}
        for reindeer, (_, duration, _) in reindeers.items()
    }
    time = 0
    while time < time_limit:
        for name, timers in reindeer_timers.items():
            update_reindeer(name, timers, distances, reindeers)
        leader_distance = max(distances.values())
        leaders = [reindeer for reindeer, distance in distances.items()
                   if distance == leader_distance]
        add_points(points, leaders)
        time += 1
    return points


def update_reindeer(reindeer, timers, distances, reindeers):
    """Update reindeer timers and distance if needed."""
    speed, duration, rest = reindeers[reindeer]
    pass_time(reindeer, timers, distances, speed)
    check_timers(timers, duration, rest)


def check_timers(timers, duration, rest):
    """Check timers if one of them run out."""
    if timers['duration'] == 0:
        change_timer(timers, 'duration', 'rest', rest)
    elif timers['rest'] == 0:
        change_timer(timers, 'rest', 'duration', duration)


def pass_time(name, timers, distances, speed):
    """Pass one unit of time from the times for working timer.

    If needed update distances for name."""
    if timers['duration'] > 0:
        timers['duration'] -= 1
        distances[name] += speed
    else:
        timers['rest'] -= 1


def change_timer(timers, turn_off_key, time_key, value):
    """Change working timer, set time_key to value and turn_off_key to -1."""
    timers[time_key] = value
    timers[turn_off_key] = -1


def add_points(points, reindeers):
    """Add point to points for each reindeer in reindeers list."""
    for reindeer in reindeers:
        points[reindeer] += 1


def fly_for(time_limit, reindeers):
    """Calculate distance traveled by each reindeer in time_limit."""
    distances = []
    for reindeer, (speed, duration, rest) in reindeers.items():
        total_time = duration + rest
        full_cycles = time_limit // total_time
        distance_in_full_cycles = speed * duration * full_cycles

        time_rest = time_limit - full_cycles * total_time
        if time_rest > duration:
            time_rest = duration

        additional_distance = speed * time_rest
        total_distance = distance_in_full_cycles + additional_distance
        distances.append((reindeer, total_distance))
    return distances


def parse_reindeers(lines):
    """Parse lines to dict of reindeers."""
    return dict(parse_reindeer(reindeer)
                for reindeer in lines)


def parse_reindeer(line):
    """Parse line with reindeer to reinder representation."""
    name, *rest_line = line.split()
    speed, duration, rest = [int(rest_line[index]) for index in (2, 5, -2)]
    return name, (speed, duration, rest)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
