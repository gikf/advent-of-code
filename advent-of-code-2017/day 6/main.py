"""Advent of Code 2017 Day 6."""


def main(file_input='input.txt'):
    blocks = [int(num) for num in get_file_contents(file_input)[0].split()]
    cycles, cycles_in_loop = find_infinite_loop(blocks)
    print(f'Cycles until repeating state: {cycles}')
    print(f'Cycles in infinite loop: {cycles_in_loop}')


def find_infinite_loop(blocks):
    """Redistribute block with highest value until reaching infinite loop."""
    cur_blocks = blocks[:]
    block_to_cycle = {}
    seen = set()
    cycles = 0
    while (blocks_state := tuple(cur_blocks)) not in seen:
        seen.add(blocks_state)
        cycles += 1
        block_to_cycle[blocks_state] = cycles
        value = max(cur_blocks)
        cur_block = cur_blocks.index(value)
        cur_blocks[cur_block] = 0
        while value > 0:
            cur_block = (cur_block + 1) % len(blocks)
            cur_blocks[cur_block] += 1
            value -= 1
    return cycles, cycles - block_to_cycle[blocks_state] + 1


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
