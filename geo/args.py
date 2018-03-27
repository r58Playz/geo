import argparse

from enum import IntEnum
from terminaltables import SingleTable

from geo import LOCATIONS


class Verbosity(IntEnum):
    QUIET = 0
    ERROR = 1
    DEBUG = 2


MAX_VERBOSITY = len(Verbosity) - 1


def location(arg):
    try:
        # Because, for argparse, text starting with - is treated as a separate
        # flag/argument, and the -- pseudo-argument doesn't help here.
        x, y = arg.replace('_', '-').split(',')
        return (float(x), float(y))
    except ValueError:
        pass

    try:
        return LOCATIONS[arg]
    except KeyError:
        raise ValueError()


class LoadLocations(argparse.Action):
    def __call__(self, parser, args, value, opt=None):
        try:
            with open(value, 'r') as file:
                for line in file.readlines():
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    if args.verbose >= Verbosity.DEBUG:
                        print('Parsing line:', line)

                    name, x, y = line.split()
                    x, y = float(x), float(y)

                    if name in LOCATIONS:
                        print(f'Warning: overwriting location {name}.')

                    LOCATIONS[name] = (x, y)
        except Exception as err:
            if args.verbose >= Verbosity.ERROR:
                raise
            else:
                print(f'Load error: {err}')
                exit(1)


class ShowLocations(argparse.Action):
    def __call__(self, parser, args, value, opt=None):
        data = [('Name', 'X', 'Y')]

        for k, v in sorted(LOCATIONS.items()):
            data.append((k, *v))

        table = SingleTable(data, 'Location Database')
        table.justify_columns[0] = 'center'
        table.justify_columns[1] = 'right'
        table.justify_columns[2] = 'right'

        print(table.table)
        print('Total:', len(LOCATIONS))

        exit()


class IncreaseVerbosity(argparse.Action):
    warned_once = False

    def __call__(self, parser, args, value, opt=None):
        old = getattr(args, self.dest)

        if not self.warned_once and old >= MAX_VERBOSITY:
            print('Warning: using -v/--verbose more than '
                  f'{MAX_VERBOSITY} times has no effect.')
            self.warned_once = True
            return

        setattr(args, self.dest, old + 1)


parser = argparse.ArgumentParser(
    prog='geo',
    description='Find your way between two locations in Minecraft.',
)

parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s 0.2.1-alpha',  # FIXME: Shouldn't be here.
)

parser.add_argument(
    '-v', '--verbose',
    help='increase debug level (1: error, 2: debug)',
    nargs=0,
    action=IncreaseVerbosity,
    default=0,
)

parser.add_argument(
    'source',
    help='the starting point',
    type=location,
    metavar='SOURCE',
)

parser.add_argument(
    'destination',
    help='the end point',
    type=location,
    metavar='DESTINATION',
)

parser.add_argument(
    '-l', '--locations',
    help='load additional locations from a file',
    action=LoadLocations,
    metavar='FILE',
)

parser.add_argument(
    '-L', '--list',
    help='list all loaded locations and exit',
    action=ShowLocations,
    nargs=0,
)
