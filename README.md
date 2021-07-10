# INE5426

## Requirements

This project uses [Poetry](https://python-poetry.org/) to handle its dependencies. If you don't have Poetry installed, you can do so following these [instructions](https://python-poetry.org/docs/#installation)

Otherwise, if you have `curl`, this project's Makefile provides a method of installing Poetry through `curl`, as instructed in the official documentations. To do that, run the command `make install-poetry`

## Usage
- Run `make all` to install Poetry and the project's dependencies, and run all three example files;

Or you can execute each step individually:
- Run `make install-poetry` to install Poetry;
- Run `make install` to use Poetry to install the project's dependencies;
- Run `make run` to execute all 3 example programs. After the execution, the results will be stored inside the `output/` folder;
- Run `make example src=<path/to/source_code` to execute the lexical analyzer on the source code provided. If you don't specify a src, the file used will be `examples/tests/success.lua`;
- To remove all files from the output/ folder, run `make clean`;
- To uninstall Poetry, run `make uninstall`.

## Examples
The three programs written in CC-2021-1 are in the `source_code` directory, alongside a few simpler examples, in the `moodle` subdirectory.
