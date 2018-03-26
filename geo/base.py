import numpy as np


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

DIRECTIONS = '''
    E ESE SE SSE
    S SSW SW WSW
    W WNW NW NNW
    N NNE NE ENE
'''.split()

TIME_UNITS = [
    ('y', 60 * 60 * 24 * 365),
    ('d', 60 * 60 * 24),
    ('h', 60 * 60),
    ('min', 60),
    ('s', 1),
]

# Blocks (meters) per second.
SPEED = [
    ('Walking', 4.3),
    ('Sprinting', 5.6),
    ('Swiming', 2.2),

    ('Minecart', 8.0),
    ('Boat', 6.5),

    ('Flying (W)', 11.0),
    ('Flying (S)', 22.0),
]

SPEED.sort(key=lambda x: x[1], reverse=True)


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def distance(point1, point2):
    delta = np.subtract(point1, point2)
    return np.sqrt(np.dot(delta, delta))


def angle_between(source, target):
    if source == target:
        return None
    delta = np.subtract(target, source)
    if delta.size != 2:
        raise ValueError('inputs must be 2D')
    return np.arctan2(delta[1], delta[0]) % (2 * np.pi)


def direction(source, target):
    angle = angle_between(source, target)

    sector = 2 * np.pi / len(DIRECTIONS)

    for i, name in enumerate(DIRECTIONS):
        mid = i * sector
        low = (mid - sector / 2) % (2 * np.pi)
        hig = (mid + sector / 2) % (2 * np.pi)
        if low > hig:
            if angle > low or angle <= hig:
                return name
        else:
            if angle > low and angle <= hig:
                return name

    raise AssertionError()


def direction_name(direction):
    if len(direction) == 3:
        a = direction_name(direction[0])
        b = direction_name(direction[1:])
        return f'{a}-{b}'
    elif len(direction) == 2:
        a = direction_name(direction[0])
        b = direction_name(direction[1]).lower()
        return f'{a}{b}'
    elif len(direction) == 1:
        if direction == 'E':
            return 'East'
        elif direction == 'S':
            return 'South'
        elif direction == 'W':
            return 'West'
        elif direction == 'N':
            return 'North'

    raise ValueError(f'invalid direction "{direction}"')


def time(seconds):
    parts = []

    while seconds > 0:
        for (t, n) in TIME_UNITS:
            if seconds >= n:
                d = int(seconds // n)
                seconds = seconds % n
                parts.append(f'{d}{t}')
                continue

        # If the time is too small to fit any unit, discard it.
        break

    if len(parts) == 0:
        return 'Now'
    else:
        return ' '.join(parts)
