"""Advent of Code 2016 Day 10."""
from collections import defaultdict, deque
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    instructions = parse_instructions(lines)
    initial_instructions = [instruction for instruction in instructions
                            if len(instruction) == 2]
    rest_instructions = [instruction for instruction in instructions
                         if len(instruction) != 2]
    bins = fill_bins(initial_instructions)
    log = process(rest_instructions, bins)
    bot = [entry
           for entry in log
           if ' 61 ' in entry and ' 17 ' in entry][0].split()[0]
    print(f'Bot responsible for comparing chips with value 61 and 17: {bot}')
    multiplied = (bins['output'][0][0]
                  * bins['output'][1][0]
                  * bins['output'][2][0])
    print(f'Multiplied values of chips in output 0, 1, 2: {multiplied}')


def process(instructions, bins):
    """Process instructions on bins."""
    log = []
    queue = deque(instructions)
    while queue:
        cur_instruction = queue.popleft()
        (_, bot), (low_type, low), (high_type, high) = cur_instruction
        bot_chips = bins['bot'][bot]
        if len(bot_chips) != 2:
            queue.append(cur_instruction)
            continue
        bins['bot'][bot] = []
        low_value, high_value = sorted(bot_chips)
        values = [(low_value, low_type, low),
                  (high_value, high_type, high)]
        add_to_bin(bins, values)
        log.append(get_log_entry(bot, values))
    return log


def get_log_entry(bot, values):
    """Prepare log entry from values."""
    sub_entries = []
    for value, bin_type, bin in values:
        sub_entries.append(f'{bot} {value} -> {bin_type} {bin}')
    return f"{bot} {', '.join(sub_entries)}"


def add_to_bin(bins, values):
    """Add values to bin."""
    for value, bin_type, bin in values:
        bins[bin_type][bin].append(value)


def fill_bins(instructions):
    """Follow instructions and fill bins."""
    bins = {'bot': defaultdict(list),
            'output': defaultdict(list)}
    for bot, value in instructions:
        bins['bot'][bot].append(value)
    return bins


def parse_instructions(lines):
    """Parse lines to instructions."""
    return [parse_instruction(line) for line in lines]


def parse_instruction(line):
    """Parse line to instruction."""
    if line.startswith('value'):
        value, bot = [
            int(num) for num in re.findall(r'(\d+).*?(\d+)', line)[0]]
        return bot, value
    bot, target_low, target_high = [
        [func(value) for func, value in zip((str, int), match.split())]
        for match in re.findall(r'(\w+ \d+).*?(\w+ \d+).*?(\w+ \d+)', line)[0]]
    return bot, target_low, target_high


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
