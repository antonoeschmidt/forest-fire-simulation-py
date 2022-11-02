# Forest fire simulation

## 02223 Model-Based Systems Engineering

# Getting started

## Requirements

* [Python 3](https://www.python.org/downloads/) (>= 3.10)
* _Soft_: [taskfile.dev](https://taskfile.dev/installation/) >=3

## Run tests
`task test` or `python -m unittest discover`(Remember to use project python).

## Run simulation with websocket
`task run` or `python simulation.py` (Remember to use project python).

## Initial setup

_Run `task init` to do the steps below._

1. _Optional_: Create a virtual environment called `.mbse` by executing `python -m venv .mbse` in the project root.
2. _Optional_: Activate the virtual environment:
    * **Windows**: `.\.mbse\Scripts\activate`
    * **Linux**/**MacOS**: `. ./.mbse/bin/activate` or `source ./.mbse/bin/activate`

   The activation script might have to be made executable:
    * **
      Windows**: `PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` [source](https://docs.python.org/3/library/venv.html#venv-def)
    * **Linux**/**MacOS**: `chmod +x ./.mbse/bin/[activate|deactivate]`

   The virtual environment can be deactivated by executing `deactivate`.
3. Install the requirements: `pip install -r requirements.txt`
4. Run `pip install -e .` to install this project as a local package
5. Everything have been set up, remember to execute the code within a terminal with the activated virtual environment.

[Python Virtual Environment](https://docs.python.org/3/library/venv.html) is a way to separate Python Packages in your
development environment. Without an environment, all Python projects use global installed packages, i.e. they all use
the same version. Upgrading a pacakge might break other projects (or this project). Instead, the packages can be
installed in a virtual environment.

## Adding a Python Package
_With task: `task install -- <package-id>`_
1. `pip install <package-id>`
2. `pip freeze > requirements.txt` - to ensure others knows which packages are expected

## Troubleshooting

### Package is missing?

Somebody might have added a dependency, run `pip install requirements.txt` (`task install-reqs`) to ensure all the required packages are
installed.

# Base variables
- Grid size: 100m x 100m
- Tick length: 5 minutes
- Base fire spread: 5 km/h
