# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:27:30 2020
"""

import re


def main():
    program = [line.strip() for line in get_file_contents()]
    memory = execute_program(program)
    sum_values = sum(memory.values())
    print(sum_values)
    memory_address_decoder = execute_memory_address_decoder(program)
    sum_values = sum(memory_address_decoder.values())
    print(sum_values)


def execute_memory_address_decoder(program):
    """Execute program as a memory address decoder."""
    memory = {}
    mask = ''
    for line in program:
        if line.startswith('mask'):
            mask = parse_mask(line)
        else:
            address, value = parse_assignment_line(line)
            result_address = decode_address(mask, address, 36)
            assert len(result_address) == 36
            addresses = []
            get_addresses(addresses, result_address, '')
            write_addresses(memory, addresses, value)
    return memory


def decode_address(mask, address, bits):
    """Use mask to decode address, with bits number of bits."""
    result_address = []
    for mask_bit, address_bit in zip(mask, pad_number(address, bits)):
        if mask_bit in 'X1':
            result_bit = mask_bit
        else:
            result_bit = address_bit
        result_address.append(result_bit)
    return result_address


def get_addresses(addresses, result_address, cur_address):
    """Generate possible addresses, replacing X with both 1 and 0."""
    if len(cur_address) == 36:
        addresses.append(cur_address)
        return
    if result_address[0] != 'X':
        get_addresses(
            addresses, result_address[1:], cur_address + result_address[0]
        )
    else:
        get_addresses(addresses, result_address[1:], cur_address + '0')
        get_addresses(addresses, result_address[1:], cur_address + '1')


def get_addresses_iterative(result_address):
    """Iterative generating possible addresses, replacing X with both
    0 and 1."""
    addresses = ['']
    for char in result_address:
        add = []
        if char != 'X':
            add.append(char)
        else:
            add.append('0')
            add.append('1')
        new_addresses = []
        for new_char in add:
            for address in addresses:
                new_addresses.append(address + new_char)
        addresses = new_addresses
    return addresses


def write_addresses(memory, addresses, value):
    """Write value to addresses in memory."""
    for address in addresses:
        memory[int(address, 2)] = value


def execute_program(program):
    """Execute program, with mask changing the values."""
    memory = {}
    mask = ''
    for line in program:
        if line.startswith('mask'):
            mask = parse_mask(line)
        else:
            result_bits = []
            address, value = parse_assignment_line(line)
            for mask_bit, value_bit in zip(mask, pad_number(value, 36)):
                if mask_bit == 'X':
                    result_bit = value_bit
                else:
                    result_bit = mask_bit
                result_bits.append(result_bit)
            assert len(result_bits) == 36
            result = int(''.join(result_bits), 2)
            memory[address] = result
    return memory


def parse_assignment_line(line):
    """Parse assignment line.

    >>>mem[42] = 100
    [42, 100]
    """
    return [
        int(num)
        for num in re.findall(r'\w+\[(\d+)\] = (\d+)', line)[0]
    ]


def parse_mask(line):
    """Parse mask line.

    >>>mask = 000000000000000000000000000000X1001X
    000000000000000000000000000000X1001X
    """
    return line.split('=')[1].strip()


def pad_number(number, bits):
    """Pad integer number to bits after converting to binary."""
    return f'{bin(number)[2:]:0>{bits}}'


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
