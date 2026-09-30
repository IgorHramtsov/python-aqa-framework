import pytest

from api.pet_client import PetClient
from data.pet_factory import create_pet_payload

from playwright.sync_api import Page

from playwright.sync_api import Playwright

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout.checkout_complete_page import CheckoutCompletePage
from pages.checkout.checkout_information_page import CheckoutInformationPage
from pages.checkout.checkout_overview_page import CheckoutOverviewPage


@pytest.fixture
def pet_client():
    return PetClient()


@pytest.fixture
def created_pet(pet_client):
    payload = create_pet_payload()
    response = pet_client.create_pet(payload)

    assert response.status_code == 200, (
        f"Failed to create pet in setup. "
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    yield payload

    pet_client.delete_pet(payload["id"])


@pytest.fixture(scope="session", autouse=True)
def configure_playwright(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page):
    return CartPage(page)


@pytest.fixture
def checkout_complete_page(page: Page):
    return CheckoutCompletePage(page)


@pytest.fixture
def checkout_information_page(page: Page):
    return CheckoutInformationPage(page)


@pytest.fixture
def checkout_overview_page(page: Page):
    return CheckoutOverviewPage(page)
