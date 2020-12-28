# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 09:24:26 2020
"""


def main():
    departure, schedule_data = [
        line.strip() for line in get_file_contents()
    ]
    earliest_possible_departure, schedule = [
        func(data) for data, func in zip(
            (departure, schedule_data), (int, parse_schedule)
        )
    ]
    print(earliest_possible_departure)
    print(schedule)
    departure, bus = find_bus(earliest_possible_departure, schedule)
    print(f'Bus: {bus} at {departure}')
    wait_time = departure - earliest_possible_departure
    print(f'Wait tiem: {wait_time}; bus x wait_time: {bus * wait_time}')
    schedule_with_breaks = parse_schedule_with_breaks(schedule_data)
    print(schedule_with_breaks)
    earliest_timestamp = find_timestamp(schedule_with_breaks)
    print('Earliest timestamp such that all of the listed bus IDs depart '
          'at offsets matching their positions in the list: '
          f'{earliest_timestamp}')


def parse_schedule(schedule_data):
    """Simple parse schedule_data.

    Return list of bus numbers. Bus number represents time between bus
    departures"""
    return [int(bus) for bus in schedule_data.split(',') if bus.isdigit()]


def parse_schedule_with_breaks(schedule_data):
    """Parse schedule_data.

    Return list of tuples having delay in deparing to the first bus in list
    and bus number. Bus number represents as welll time between bus
    departures."""
    return [
        (delay_in_departing, int(bus))
        for delay_in_departing, bus in enumerate(schedule_data.split(','))
        if bus.isdigit()
    ]


def find_timestamp_slow(schedule):
    """Find earliest departure timestamp, when busses depart at offsets
    matching position in list.

    Not very efficient for big list."""
    first_departure, first_bus = max(schedule, key=lambda item: item[1])
    relative_schedule = [
        (minute - first_departure, bus)
        for minute, bus in schedule
    ]
    timestamp = 0
    while True:
        for minute, bus in sorted(
            relative_schedule, key=lambda item: item[1], reverse=True
        ):
            cur_timestamp = timestamp + minute
            if cur_timestamp % bus != 0:
                break
        else:
            return timestamp - first_departure
        timestamp += first_bus
    return timestamp


def find_timestamp(schedule):
    """Find earliest departure timestamp, when busses depart at offsets
    matching their position in schedule list.

    Based on properties shown by:
    https://www.reddit.com/r/adventofcode/comments/kc60ri/2020_day_13_can_anyone_give_me_a_hint_for_part_2/gfnnfm3/
    """
    first_departure, first_bus = max(schedule, key=lambda item: item[1])
    busses = [schedule[0][1]]
    timestamp = 0
    for index, (minute, bus) in enumerate(schedule[:-1]):
        next_departure, next_bus = schedule[index + 1]
        cur_increment = product(busses)
        while (timestamp + next_departure) % next_bus != 0:
            timestamp += cur_increment
        busses.append(next_bus)
    return timestamp


def product(numbers):
    """Calculate product of numbers."""
    result = 1
    for number in numbers:
        result *= number
    return result


def find_bus(earliest_departure, busses):
    """Find bus from busses deparing earliest after earliest_departure."""
    next_departures = [
        (next_departure_after(earliest_departure, bus), bus) for bus in busses
    ]
    return sorted(next_departures)[0]


def next_departure_after(time, bus):
    """Return next bus departure after time."""
    return time - (time % bus) + bus


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
