# INE5426

## Requirements

This project uses [Poetry](https://python-poetry.org/) to handle its dependencies. IF you don't have Poetry installed, you can do so following these [instructions](https://python-poetry.org/docs/#installation)

Otherwise, if you have `curl`, this project's Makefile provides a method of installing Poetry through `curl`, as instructed in the official documentations. To do that, run the command `make install-poetry`

## Usage
- Run `make install-poetry` if you'd like;
- Run `make install` to use Poetry to install the project's dependencies;
- Run `make run src=<path/to/source_code` to execute the lexical analyzer on the source code provided. If you don't specify a src, the file used will be `examples/tests/success.lua`.
- Afterwards, if you wish to uninstall Poetry, run `make clean`

## Examples
The three programs written in CC-2021-1 are in the `source_code` directory, alongside a few simpler examples, in the `moodle` subdirectory.
