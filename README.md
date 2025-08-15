# STORASENSE
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

### Environments
This project has been configured with
[Environments](.env.example)
for managing environment variables. The `.env` file should be created in the root directory of the project, and it should contain the necessary environment variables for the application to run. The `.env.example` file serves as a template for the `.env` file, providing a reference for the required variables.
An important variable is the ENVIRONMENT variable, which should be set to one of the following values:
- `DEV` for local development;
- `PROD` for production;
- `TEST` for testing.
#### Database Configuration
- While `PROD` establish an empty database (seeded with known sensors), `DEV` will create a database with random generated data for testing purposes.
- The `TEST` environment is used for running automated tests and should not be used for development or production - data will be setup and removed automatically by the test suite.

Note: When switchting from `DEV` to `PROD`, you have to run the following command to reset the database schema:
```bash
    docker compose exec timescaledb /docker-entrypoint-initdb.d/reset-app-db.sh
```
or

```bash
    just reset-db # if you have installed the `just` command line tool.
```

---

## Deployment Workflow:
### 1.  DNS Configuration
- Create a DNS record for `storasense.de` in your OS pointing to the server's IP address (loopback-adress): `127.0.0.1 storasense.de api.storasense.de auth.storasense.de traefik.storasense.de`
### 2. .env Configuration
- Verify `.env` configuration (root directory) - checkout `.env.example` for reference.
### 3. Docker Configuration
- Ensure Docker is installed and running on your system.
- Make the db-init script executable:
```bash
chmod +x ./db-init/db-init.sh
```
- Build the Docker-Compose Setup: `docker-compose up -d --build`
### 4. Optional: Keycloak Configuration
- If you don't have our original volume of the timescaledb (**storasense_data_volume**) then you have to setup the Keycloak configuration from scratch by yourself.
- Follow the following steps:
  * Create an initial **temporary admin user** - add to the `docker-compose.yml` configuration: `keycloak: environment:`:
  ```yaml
    - KEYCLOAK_ADMIN=admin # or use a .env variable
    - KEYCLOAK_ADMIN_PASSWORD=admin # or use a .env variable
  ```
  * Open the Keycloak Admin Console in your browser at `http://localhost:8088/admin`.
  * Login with the temporary admin user credentials you set in the first step.
  * Create a new realm named `storasense-realm`.
  * Create three new clients - for the **backend**, **frontend** and **mqtt-client** - with the following settings:
    * Client ID: `fastapi-backend-client` / `frontend-client` / `mqtt-client`
    * Name: `STORASENSE-Backend` / `STORASENSE-Frontend` / `STORASENSE-MQTT`
    * `Client authentication` should be disabled - except for the **mqtt-client**.
    * `Standard flow` and `Direct access grants` should be enabled - except for the **mqtt-client**.
    * For Backend:
      - Add `Valid redirect URIs`: `https://api.storasense.de/docs/oauth2-redirect` and `http://localhost:*`
      - Add `Web Origins`: `https://storasense.de` and `https://api.storasense.de`
    * For Frontend:
      - Add `Valid redirect URIs`: `https://storasense.de/*` and `https://auth.storasense.de/`
      - Add `Valid post logout redirect URIs`: `https://storasense.de/*`
      - Add `Web Origins`: `https://storasense.de`
    * For MQTT:
      - Enable `Client authentication`
      - Enable `Service accounts roles`
      - Copy the `Client secret` (go to `Credentials` section) after saving the client configuration.
  * Add Client-Mapping regarding Audience: Go to Clients -> fastapi-backend-client / frontend-client / mqtt-client -> Client scopes -> fastapi-backend-client-... / frontend-client-... / mqtt-client-... -> Add mapper -> Configure the following:
    * Mapper Type: `Audience`
    * Name: `audience-mapper-storasense-be`/ ...
    * Included Client Audience: `fastapi-backend-client`
    * Add to access token: `enabled`
  * Configure the roles and user groups as needed.
  * Setup a user with the role `admin` in the `storasense-realm`.
  * Configure optionally identity providers (e.g., Google, GitHub).
  * Make sure that the **User profile attributes** (go to `Realm settings` -> `User profile`) match with our database schema (except the intern managed attributes - such as the ids).
  * Remove the temporary admin user from the `docker-compose.yml` file after the initial setup is completed.
---
## URLs:
| URL Type                                   | URL                                                                                                                             |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Frontend                                   | [https://storasense.de](https://storasense.de)
| Backend-API Documentation <br> (SwaggerUI) | [https://api.storasense.de/docs](https://api.storasense.de/docs)                                                                |
| Keycloak-Configuration / Admin-Console     | [https://auth.storasense.de](https://auth.storasense.de) / [https://auth.storasense.de/admin](https://auth.storasense.de/admin) |
| Traefik Dashboard                           | [https://traefik.storasense.de](https://traefik.storasense.de)                                                                  |
