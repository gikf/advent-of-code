"""Advent of Code 2017 Day 9."""


def main(file_input='input.txt'):
    streams = [line.strip() for line in get_file_contents(file_input)]
    score, garbage_chars = analyse_streams(streams)
    print(f'Total score in groups in streams: {score}')
    print(f'Non-cancelled characters in garbage: {garbage_chars}')


def analyse_streams(streams):
    """Return score and garbage_chars of streams."""
    score = 0
    garbage_chars = 0
    for stream in streams:
        stream_score, stream_garbage = analyse_stream(stream)
        score += stream_score
        garbage_chars += stream_garbage
    return score, garbage_chars


def analyse_stream(stream):
    """Analyse stream and return state score and number of garbage chars."""
    state = get_state()
    for char in stream:
        for condition, (action, params) in get_actions():
            if condition(char, state):
                action(state, *params)
                break
    return state['score'], state['garbage_chars']


def get_state():
    """Get fresh state."""
    return {
        'score': 0,
        'score_level': 0,
        'garbage_chars': 0,
        'garbage': False,
        'cancel': False,
        'stack': [],
    }


def get_actions():
    """Yield next possible action."""
    actions = [
        (lambda char, state: state['cancel'], (handle_set, ('cancel', False))),
        (lambda char, state: char == '!', (handle_set, ('cancel', True))),
        (lambda char, state: state['garbage'] and char == '>',
         (handle_set, ('garbage', False))),
        (lambda char, state: state['garbage'] and char != '>',
         (increment_garbage, ())),
        (lambda char, state: char == '{', (handle_open, ())),
        (is_closing_char, (handle_close, ())),
        (lambda char, state: char == '<', (handle_set, ('garbage', True))),
    ]
    yield from actions


def increment_garbage(state):
    """Decrement garbage_chars in state."""
    state['garbage_chars'] += 1


def handle_open(state):
    """Handle open bracket on state."""
    state['stack'].append('{')
    state['score_level'] += 1


def handle_close(state):
    """Handle closing bracket on state."""
    state['stack'].pop()
    state['score'] += state['score_level']
    state['score_level'] -= 1


def handle_set(state, parameter, value):
    """Set parameter in state to value."""
    state[parameter] = value


def is_closing_char(char, state):
    """Check if closing char should be processed."""
    return char == '}' and state['stack'] and state['stack'][-1] == '{'


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
