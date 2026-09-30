import pytest
import allure
from helpers.ui_helpers import login_and_check_inventory

from data.constants import (
    STANDARD_USER,
    LOCKED_OUT_USER,
    PASSWORD,
    INVALID_PASSWORD,
    INVALID_CREDENTIALS_ERROR,
    LOCKED_OUT_ERROR,
    SORT_NAME_ASC,
    SORT_NAME_DESC,
    SORT_PRICE_ASC,
    SORT_PRICE_DESC,
    SUCCESSFUL_ORDER,
    COMMENT_FOR_SUCCESSFUL_ORDER,
    ERROR_FOR_CHECKOUT_FORM
)

pytestmark = pytest.mark.ui


@allure.feature("Authentication")
@allure.title("Successful login")
@pytest.mark.smoke
def test_successful_login(login_page, inventory_page):
    login_page.open_login_page()
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.header.check_title_and_page_opened("Products")


@pytest.mark.smoke
def test_login_with_invalid_password(login_page):
    login_page.open_login_page()
    login_page.login(STANDARD_USER, INVALID_PASSWORD)
    login_page.check_error_message(INVALID_CREDENTIALS_ERROR)


def test_locked_out_user_login(login_page):
    login_page.open_login_page()
    login_page.login(LOCKED_OUT_USER, PASSWORD)
    login_page.check_error_message(LOCKED_OUT_ERROR)


def test_add_one_product_to_cart(login_page, inventory_page, cart_page):
    product_index = 0
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(product_index)
    name1 = inventory_page.get_product_name(product_index)
    price1 = inventory_page.get_product_price(product_index)
    inventory_page.check_shopping_cart_badge(1)
    inventory_page.navigate_to_shopping_cart()
    name2 = cart_page.get_product_name(product_index)
    price2 = cart_page.get_product_price(product_index)
    assert name2 == name1
    assert price2 == price1


def test_add_several_products_to_cart(login_page, inventory_page):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(0)
    inventory_page.add_product_to_cart(1)
    inventory_page.check_shopping_cart_badge(2)


def test_add_product_and_delete_from_cart(login_page, inventory_page, cart_page):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(0)
    inventory_page.check_shopping_cart_badge(1)
    inventory_page.navigate_to_shopping_cart()
    cart_page.remove_product_from_shopping_cart()
    cart_page.back_to_inventory_page()
    inventory_page.check_shopping_cart_empty()


@pytest.mark.parametrize("sort_option, sort_type, reverse", [
    (SORT_NAME_ASC, "name", False),
    (SORT_NAME_DESC, "name", True),
    (SORT_PRICE_ASC, "price", False),
    (SORT_PRICE_DESC, "price", True),
])
def test_sorting_for_each_option(login_page, inventory_page, sort_option, sort_type,
                                 reverse):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.sort_products(sort_option)

    if sort_type == "name":
        inventory_page.check_products_sorted_by_name(reverse)
    else:
        inventory_page.check_products_sorted_by_price(reverse)


@allure.feature("Checkout")
@allure.story("Successful order")
@allure.title("User can successfully complete checkout")
@pytest.mark.smoke
def test_successful_order(login_page, inventory_page, cart_page, checkout_information_page, checkout_complete_page,
                          checkout_overview_page):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(0)
    inventory_page.check_shopping_cart_badge(1)
    inventory_page.navigate_to_shopping_cart()
    cart_page.click_checkout_button()
    checkout_information_page.fill_information_form("1", "1", "1")
    checkout_information_page.click_continue_button()
    checkout_overview_page.click_finish_button()
    checkout_complete_page.check_order_is_successful(SUCCESSFUL_ORDER, COMMENT_FOR_SUCCESSFUL_ORDER)


def test_checkout_without_data(login_page, inventory_page, cart_page, checkout_information_page):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(0)
    inventory_page.check_shopping_cart_badge(1)
    inventory_page.navigate_to_shopping_cart()
    cart_page.click_checkout_button()
    checkout_information_page.click_continue_button()
    checkout_information_page.check_form_error_is_displayed()
    checkout_information_page.check_form_error_message(ERROR_FOR_CHECKOUT_FORM)
