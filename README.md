# Project
***
## Setup:
- Python version: **3.13**
- Setup a virtual environment:
***
```bash
python -m venv .venv
```
- Activate the virtual environment:
  - On Windows:
    ```bash
    .venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```
***
- Change interpreter in your IDE to the virtual environment.
- Install Poetry if not already installed:
```bash
pip install poetry
```
- Install dependencies:
```bash
poetry install
```
***


## Development Workflow:

### Pre-Commit Hooks

This project utilises pre-commit hooks. To install them locally, execute the following two lines:

```bash
pre-commit install
```

```bash
pre-commit install --hook-type commit-msg --hook-type pre-push
```

and execute the following line to run all pre-commit hooks:

```bash
pre-commit run --all-files
```

### Branches and Branch Naming

For development, always create a new branch from `dev` and name it with the following convention:
```
<type>/<description>
```
Where `type` is a type explained below in the section about commit messages and `description` is a short
description abut the branch contents, in kebab-case.

### About Commit Styles

Commit messages have been configured in accordance with
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
and should follow the following format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

where `type` is one of the following:
- `feat` for features;
- `fix` for patches and bug fixes;
- `refactor` for code refactoring;
- `test` for automated tests;
- `docs` for documentation;
- further legal values are `build`, `chore`, `ci`, `style`, and `perf`.


### Semantic Release

This project has been configured with
[Python Semantic Release](https://github.com/python-semantic-release/python-semantic-release)
for automatically creating a release version after commits to the `main` branch. Release notes
are inferred from the formatted commit messages.
