import numpy as np

from terminaltables import SingleTable

from base import (
    SPEED,
    distance,
    angle_between,
    direction,
    direction_name,
    time,
)


# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------

# FIXME: Isn't really constant. Should probably be a parameter instead.
LOCATIONS = {
    'origin': (0, 0),

    'far+': (1000, 1000),
    'far-': (-1000, -1000),

    'border+': (14_999_992, 14_999_992),
    'border-': (-14_999_992, -14_999_992),
}


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

# TODO: Use thousands separators in the distance.
#       Maybe even in the coordinates.
def travel(source, target):
    d = distance(source, target)

    if d == 0.0:
        a = 'N/A'
        h = 'N/A'
        H = 'N/A'
    else:
        a = angle_between(source, target)
        a = np.round(np.rad2deg(a))
        a = f'{a:.0f}°'
        h = direction(source, target)
        H = direction_name(h)

    table = SingleTable([
        ('Source', source),
        ('Destination', target),
        ('Distance', f'{d:.2f}'),
        ('Angle', a),
        ('Direction', h),
        ('', H),
    ], 'Travel Information')

    table.inner_heading_row_border = False
    table.justify_columns[0] = 'right'

    print(table.table)
    # print()

    data = [
        ('Method', 'ETA'),
    ]

    # SPEED is already sorted.
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
