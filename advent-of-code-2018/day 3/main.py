"""Advent of Code 2018 Day 3."""


EMPTY = '.'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    claims = parse_claims(lines)
    fabric = get_square(1000)
    mark_claims(claims, fabric)
    claimed_by_more_than_two = squares_claimed_by_more_than(fabric, 2)
    print(f'Squares claimed by two or more claims: {claimed_by_more_than_two}')
    non_overlapping_claim = find_non_overlapping_claim(claims, fabric)
    print(f'ID of non-overlapping claim: {non_overlapping_claim}')


def find_non_overlapping_claim(claims, fabric):
    """Find ID of claim non-overlapping with other claims."""
    for claim_id, claim in enumerate(claims, start=1):
        if is_non_overlapping(claim, fabric):
            return claim_id
    return -1


def is_non_overlapping(claim, fabric):
    """Check if claim is overlapping."""
    for row, col in generate_coordinates(claim):
        if fabric[row][col] != 1:
            return False
    return True


def mark_claims(claims, fabric):
    """Mark claims on fabric."""
    for claim in claims:
        mark_claim(claim, fabric)


def mark_claim(claim, fabric):
    """Mark claim on fabric."""
    for row, col in generate_coordinates(claim):
        if fabric[row][col] is EMPTY:
            fabric[row][col] = 0
        fabric[row][col] += 1


def generate_coordinates(claim):
    """Generate coordinates within claimed rectangle."""
    (edge_col, edge_row), (claim_cols, claim_rows) = claim
    for row in range(edge_row, edge_row + claim_rows):
        for col in range(edge_col, edge_col + claim_cols):
            yield (row, col)


def squares_claimed_by_more_than(fabric, claims):
    """Count number of squares on fabric being claimed by number of claims."""
    return sum(
        sum(
            square is not EMPTY and square >= claims
            for square in row
        )
        for row in fabric
    )


def get_square(size):
    """Get empty square of size."""
    return [[EMPTY for _ in range(size)]
            for _ in range(size)]


def parse_claims(lines):
    """Parse claims."""
    return [parse_claim(line) for line in lines]


def parse_claim(line):
    """Parse line to tuple with edge coordinates and size of rectangle."""
    _, claim = line.split(' @ ')
    edge_part, rectangle_part = claim.split(': ')
    edge = [int(num) - 1 for num in edge_part.split(',')]
    rectangle = [int(num) for num in rectangle_part.split('x')]
    return edge, rectangle


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
