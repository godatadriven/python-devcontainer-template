# Your fantastic repo

Hi! Welcome to the team ! Let's get you started quickly. This is what you have to do.

## Installation

1. Install Java 11.0.16

1. Install Python 3.10.8

### Virtual environment
There are a couple ways to go about this.

1. `pyenv`

    First, install pyenv using the [pyenv-installer](https://github.com/pyenv/pyenv-installer).

    Then, create a new environment using:

    ```
    pyenv shell 3.10.8
    pyenv virtualenv my-venv
    pyenv shell my-venv
    ```

1. Conda

    Install conda and create a virtualenv.

1. Python venv

    ```
    python -m venv venv
    source ./venv/bin/activate
    ```

### pip packages

1. Make sure to `pip` install the following packages:

    - black
    - pytest
    - jupyter (not necessary when installing for CI or prod)
    - mypy




⚠️ Note: this is entire setup is known to work for Debian GNU/Linux 11 (bullseye), not tested for other Operating Systems.