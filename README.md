# geo

Find your way between two locations in Minecraft

**Requires Python 3**

## Usage

Aside from running `geo/__main__.py` directly, multiple user friendly ways of using geo are provided. All paths below are relative to the root of this repository:

* `bin/geo` is a sh script that assumes that it is located in a directory that also contains the `geo` folder provided in this repository. It forwards all command line arguments to geo itself.

* `zip/geo` is a sh script that assumes that `zip/geo.zip` is also located in its folder, but does not require anything from the `geo` directory to work. It is otherwise functionally identical to `bin/geo`, and forwards its arguments as well.

Running geo with the `--help` flag prints the following:

```
usage: geo [-h] [--version] [-v] [-l FILE] [-L] SOURCE DESTINATION

Find your way between two locations in Minecraft.

positional arguments:
  SOURCE                the starting point
  DESTINATION           the end point

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         increase debug level (1: error, 2: debug)
  -l FILE, --locations FILE
                        load additional locations from a file
  -L, --list            list all loaded locations and exit
```

### Positional Arguments

`SOURCE` and `DESTINATION` support two formats:

* **Coordinates**, such as `100,100`, `-50,50`, `-200,-10`, etc.
* **Names**, such as `home`, `my-castle`, etc.

As a convenience, since the `-` in the X coordinate may be interpreted by geo as an argument, it can be written as `_` instead, for the same effect (e.g. `_200,_10`).

### Location Files

The format of the `--locations` file must be as follows:

```
# This is a comment.
plains   100  200
desert  -200 1000
my-home   50 -200
...
```

Where blank lines are ignored and the arguments in each line are separated by any amount of spaces or tabs. Aligning the columns is, of course, optional.

Note that arbitrarily many such files can be provided:

`geo -l homes -l villages -l oceans ...`

## Known Issues

* When the zip binary fails and has been provided the `-v/--verbose` flag, the trace back will not include lines of source code from files in the zip itself. This is unavoidable.

## Future

* [ ] Thousands separators for distance, maybe coordinates, etc.
* [ ] Support for 3D coordinates (directions should still be 2D).
* [ ] Include dependencies in the zip file.
* [ ] More robust sh scripts.
* [ ] Windows binaries.
* [ ] Python 2 compatibility (unlikely).
* [ ] Do we really need numpy?
