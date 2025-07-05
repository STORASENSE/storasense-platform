# Project

***
## Setup: 
- Python-version: **3.13** 
- Setup a virtual environment:
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
- Always use **dev** branch as the base branch for your pull requests.
- Create a new branch for your changes from **dev** branch:
```
feature/<Ticket-ID>-<Short-Description> 
```
