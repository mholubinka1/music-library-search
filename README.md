# music-library-search




















### Modifying This Repository

### 1. Setup

- Install Python 3.11.4 or higher
- Install [poetry](https://python-poetry.org/) version 1.5.1 or higher
- Navigate into the repository to the folder containing ```pyproject.toml``` and install the dependencies
    - Create a virtual environment: ```poetry env use python```
    - Confirm that the environment has been activated: ```poetry env list``` (should have the ```(activated)``` note next to the previosuly created enviroment)
    - If the environment is not activated, activate it with: ```poetry shell```
    - Install all dependencies (in this virtual environment), including the development dependencies: ```poetry install --with dev```

### 2. Pre-Commit Setup

Code-checking and linting tools are configured to run automatically on every commit to save manual efforts.

- Install [pre-commit](https://github.com/pre-commit/pre-commit) system-wide: ```pip install pre-commit```
- Add to the git repository: ```pre-commit install```
- Run ```pre-commit run --all-file``` to execute all ```pre-commit``` hooks

### 3. Unit Testing

This application uses [pytest](https://docs.pytest.org/en/7.2.x/) as the unit testing framework with all tests stored in the ```tests``` directory.

#### 3.1. Run Tests

Run all tests with ```poetry run pytest tests```

To run tests and generate a coverage report: ```poetry run pytest tests --cov --cov-report=html --cov-branch``` (replace ```html``` with ```xml``` to a generate xml report, if preferred).
