[![pytest](https://github.com/JASMINE-Mission/telescope_baseline/actions/workflows/pytest.yml/badge.svg?branch=develop)](https://JASMINE-Mission.github.io/telescope_baseline/test_report/index.html)
[![build](https://github.com/JASMINE-Mission/telescope_baseline/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/JASMINE-Mission/telescope_baseline/actions/workflows/build.yml)

# Baseline study of the JASMINE telescope

This respository provides documents and tools to define the baseline design of the JASMINE telescope. Type the following lines to install `telescope_baseline` package in your environment.

``` console
$ git clone git@github.com:JASMINE-Mission/telescope_baseline.git
$ cd telscope_baseline
$ git checkout develop
$ git pull
$ python setup.py install
```


## Contents
The repository consists of the following components.

- `src/telescope_baseline`
- `examples`
- `snippets`
- `tests`


### Package Definitions
The directory `src/telescope_baseline` contains the following directories.

- `data`: Several measurements (filter responses etc.)
- `dataclass`: _Contents in this directory should be moved elsewhere_
- `mapping`: Functions to construct a mapping strategy.
- `obsplan`: _Contents in this directory should be moved elsewhere_
- `photometry`: Functions to estiamte a S/N ration in photometry.
- `tools`: Elementary classes.
    - `efficiency`: Provides the `Filters` class.
    - `mission`: Provides the `Parameters` class.
- `utils`: _Contents in this directory should be moved elsewhere_


### Examples
Example codes are stored in this directory.


### Snippets
Snippets to prepare data and to generate images are stored in `snippets`.


### Tests
Test cases are provided in the `tests` directory. We use `pytest` to check the code itegrity. Install `pytest` via `pip` and type the following line to test the code. _Do not forget to test the code before making a pull request._

``` console
$ cd tests
$ pytest
```
