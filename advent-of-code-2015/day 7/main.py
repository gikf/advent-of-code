"""Advent of Code 2015 Day 7."""


def main(file_input='input.txt'):
    input_connections = [
        line.strip() for line in get_file_contents(file_input)]
    connections = parse_connections(input_connections)
    signals = set_wires(connections)
    signal_a = signals['a']
    print(f'Signal to wire a: {signal_a}')
    overriden = connections.copy()
    overriden['b'] = signal_a
    overriden_signals = set_wires(overriden)
    new_signal_a = overriden_signals['a']
    print(f'After overriding wire b with {signal_a}, '
          f'new signal to wire a: {new_signal_a}')


def set_wires(connections):
    """Set wires signal values according to the connections."""
    wires = connections.copy()
    while not all_wires_with_value(wires):
        for wire in connections:
            input_signal = wires[wire]
            if isinstance(input_signal, int):
                continue
            new_signal = process_signal(input_signal, wires)
            if is_signal_with_values(new_signal):
                wires[wire] = get_wire_signal(new_signal)
            elif input_signal != new_signal:
                wires[wire] = new_signal
    return wires


def process_signal(input_signal, wires):
    """Process input_signal, updating values if possible."""
    new_signal = []
    for signal in input_signal:
        if isinstance(signal, str) and isinstance(wires[signal], int):
            new_signal.append(wires[signal])
        else:
            new_signal.append(signal)
    return new_signal


def is_signal_with_values(signal):
    """Check if signal has all needed values for calculating output signal."""
    return all(
        not isinstance(item, str)
        for item in signal
    )


def get_wire_signal(signal):
    """Get value to set for wire based on signal"""
    if len(signal) == 1:
        return signal[0]
    elif len(signal) == 2:
        func, num = signal
        return func(num)
    elif len(signal) == 3:
        num1, func, num2 = signal
        return func(num1, num2)


def all_wires_with_value(wires):
    """Check if all wires have signal set as numeric value."""
    return all(
        isinstance(wire, int)
        for wire in wires.values()
    )


def parse_connections(input_connections):
    """Parse input_connections."""
    return dict(
        parse_connection(connection)
        for connection in input_connections
    )


def parse_connection(connection):
    """Parse connection to internal representation."""
    left, right = connection.split(' -> ')
    if left.isdigit():
        return right, int(left)
    input_signal = left.split()
    if isinstance(input_signal, str):
        return right, [input_signal]

    input_signal = [int(item) if item.isdigit() else item
                    for item in input_signal]

    if len(input_signal) == 2:
        input_signal[0] = get_bitwise_function('NOT')
    elif len(input_signal) == 3:
        input_signal[1] = get_bitwise_function(input_signal[1])
    return right, input_signal


def get_bitwise_function(bitwise):
    """Get function corresponding to the bitwise operation."""
    return {
        'AND': b_and,
        'OR': b_or,
        'NOT': b_not,
        'LSHIFT': lshift,
        'RSHIFT': rshift,
    }[bitwise]


def b_and(num1, num2):
    """Bitwise num1 and num2."""
    return num1 & num2


def b_or(num1, num2):
    """Bitwise num1 or num2."""
    return num1 | num2


def b_not(num):
    """Bitwise complement num."""
    return ~num


def lshift(num1, num2):
    """Left shift num1 by num2."""
    return num1 << num2


def rshift(num1, num2):
    """Right shift num1 by num2."""
    return num1 >> num2


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
