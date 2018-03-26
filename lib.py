import numpy as np

from terminaltables import SingleTable


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
    ('d', 60 * 60 * 24),
    ('h', 60 * 60),
    ('m', 60),
    ('s', 1),
]

# Units (meters) per second.
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
# Internal
# -----------------------------------------------------------------------------

def distance(point1, point2):
    delta = np.subtract(point1, point2)
    return np.sqrt(np.dot(delta, delta))


def angle_between(source, target):
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
        else:
            raise ValueError()
    else:
        raise ValueError()


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


# -----------------------------------------------------------------------------
# External
# -----------------------------------------------------------------------------

def travel(src, tgt):
    print(f'From "{src}" to "{tgt}":')
    print()

    source = LOCATIONS[src]
    target = LOCATIONS[tgt]

    d = distance(source, target)
    a = np.round(np.rad2deg(angle_between(source, target)))
    h = direction(source, target)

    table = SingleTable([
        ('Source', source),
        ('Destination', target),
        ('Distance', f'{d:.2f}'),
        ('Angle', f'{a:.0f}°'),
        ('Direction', h),
    ], 'Travel Information')

    table.inner_heading_row_border = False
    table.justify_columns[0] = 'right'

    print(table.table)
    print()

    print(h, ':', direction_name(h))
    print()

    data = [
        ('Method', 'ETA'),
    ]

    for (k, v) in SPEED:
        t = time(d / v)
        data.append((k, t))

    table = SingleTable(data, 'Travel Time')
    table.justify_columns[0] = 'center'
    table.justify_columns[1] = 'right'

    print(table.table)


# def show_map(scale=1):
#
#
# d**2 = x**2 + y**2
# (dF)**2 = ...
# d**2 F**2 = ...
# d**2 = (x**2 + y**2) / F**2


# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------

LOCATIONS = {
    'origin': (0, 0),
    'home.first': (-352, 193),
    'home.trees': (-483, 439),
    'home.desert': (-712, 100),

    'village': (-899, 86),

    'pillar-1': (-603, 228),
    'pillar-2': (-273, -135),

    'castle': (-822, 81),
}
