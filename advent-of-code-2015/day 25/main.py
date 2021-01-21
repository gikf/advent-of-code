"""Advent of Code 2015 Day 25."""


def main(row=2978, column=3083):
    wanted_row = row + column
    wanted_column = wanted_row
    row = fill_row([20151125] + [0] * (wanted_column - 1),
                   wanted_row, wanted_column - 1)
    print(f'Code for the machine: {row[column - 1]}')


def fill_row(codes, wanted_row, wanted_column):
    """Fill codes row with codes until wanted_row and_wanted_column."""
    cur_column = 1
    cur_row = 1
    next_column = 1
    code = codes[0]
    while cur_row != wanted_row and cur_column != wanted_column:
        code = get_next_code(code)
        if cur_column == next_column:
            cur_row = cur_column
            next_column += 1
            cur_column = 0
        codes[cur_column] = code
        cur_row -= 1
        cur_column += 1
    return codes


def fill_table(codes, wanted_row, wanted_column):
    """Fill table with codes until wanted_row and wanted_column."""
    cur_column = len(codes[0]) - 1
    cur_row = len(codes) - 1
    code = codes[0][0]
    while cur_row != wanted_row and cur_column != wanted_column:
        code = get_next_code(code)
        if len(codes) == len(codes[0]):
            cur_row = len(codes)
            cur_column = 0
            codes.append([])
        codes[cur_row].append(code)
        cur_row -= 1
        cur_column += 1
    return codes


def get_next_code(last_code):
    """Generate next code based on the last_code."""
    return (last_code * 252533) % 33554393


if __name__ == '__main__':
    main()
