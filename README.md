# Python AQA Framework

A small automation testing project built with Python, pytest and Playwright.

It contains API tests for Swagger Petstore and UI tests for SauceDemo.  
The project also includes Docker, Jenkins and Allure integration.

## Tech Stack

- Python
- pytest
- requests
- Playwright
- Allure
- Docker
- Jenkins

## Project Structure

```text
api/          API client
config/       Test configuration
data/         Test data and factories
pages/        Page Objects
tests/api/    API tests and fixtures
tests/ui/     UI tests and fixtures
```

## Test Coverage

API:
- create pet
- get pet
- update pet
- delete pet
- search by status
- negative scenarios

UI:
- login
- negative login scenarios
- product sorting
- shopping cart
- checkout validation
- successful order

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
playwright install chromium
```

## Run Tests

Run all tests:

```powershell
pytest -v
```

API tests:

```powershell
pytest -m api -v
```

UI tests:

```powershell
pytest -m ui -v
```

Smoke tests:

```powershell
pytest -m smoke -v
```

## Allure

Generate Allure results:

```powershell
pytest -v --alluredir=allure-results --clean-alluredir
```

Open the report:

```powershell
allure serve allure-results
```

## Docker

Build the image:

```powershell
docker build -t python-aqa-framework .
```

Run all tests:

```powershell
docker run --rm python-aqa-framework
```

## Jenkins

The Jenkins pipeline allows selecting `smoke`, `api`, `ui` or `all`.

It builds the Docker image, runs the selected tests and publishes the Allure report.

## Configuration

The following environment variables can be used to override the default configuration:

```text
BASE_API_URL
BASE_UI_URL
REQUEST_TIMEOUT
```

Default values are already configured, so they are not required for a normal local run.

## About

This project was created to practice building an automation framework with API and UI tests, test data management, Docker and CI integration.

The tests use public demo applications, so their availability can affect test runs.