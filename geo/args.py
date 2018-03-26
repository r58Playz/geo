import argparse

from terminaltables import SingleTable

from geo import LOCATIONS


def location(arg):
    try:
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
                    if line.isspace() or line.startswith('#'):
                        continue
                    name, x, y = line.split()
                    x, y = float(x), float(y)
                    LOCATIONS[name] = (x, y)
        except Exception as err:
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

        exit()


parser = argparse.ArgumentParser(
    prog='geo',
    description='Find your way between two locations in Minecraft.'
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
    '--list', '--list-locations',
    help='list all loaded locations, then exit',
    action=ShowLocations,
    nargs=0,
)
