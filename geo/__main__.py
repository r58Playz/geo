#!/usr/bin/env python

from geo import travel
from args import parser

if __name__ == '__main__':
    args = parser.parse_args()

    # print(f'From {args.source} to {args.destination}:')
    # print()

    travel(args.source, args.destination)
