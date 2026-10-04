import os


BASE_API_URL = os.getenv("BASE_API_URL", "https://petstore3.swagger.io/api/v3").rstrip("/")
BASE_UI_URL = os.getenv("BASE_UI_URL", "https://www.saucedemo.com/")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10"))

if REQUEST_TIMEOUT <= 0:
    raise ValueError("REQUEST_TIMEOUT must be greater than zero")
