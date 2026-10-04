from decimal import Decimal

import pytest
import allure

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
)

pytestmark = pytest.mark.ui


def login_and_check_inventory(login_page, inventory_page):
    login_page.open_login_page()
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.header.check_title_and_page_opened("Products")


@allure.feature("Authentication")
@allure.title("Successful login")
@pytest.mark.smoke
def test_successful_login(login_page, inventory_page):
    login_page.open_login_page()
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.header.check_title_and_page_opened("Products")


@pytest.mark.smoke
@pytest.mark.parametrize("username, password, expected_error", [
    pytest.param(STANDARD_USER, INVALID_PASSWORD, INVALID_CREDENTIALS_ERROR, id="invalid-password"),
    pytest.param("", PASSWORD, "Epic sadface: Username is required", id="empty-username"),
    pytest.param(STANDARD_USER, "", "Epic sadface: Password is required", id="empty-password"),
])
def test_login_with_invalid_password(login_page, username, password, expected_error):
    login_page.open_login_page()
    login_page.login(username, password)
    login_page.check_error_message(expected_error)


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
    cart_page.check_products([name1])
    price2 = cart_page.get_product_price(product_index)
    assert price2 == price1, (
        f"Price changed for {name1!r}: inventory={price1}, cart={price2}"
    )


def test_add_several_products_to_cart(login_page, inventory_page, cart_page):
    login_and_check_inventory(login_page, inventory_page)
    expected_names = [inventory_page.get_product_name(index) for index in (0, 1)]
    inventory_page.add_product_to_cart(0)
    inventory_page.add_product_to_cart(1)
    inventory_page.check_shopping_cart_badge(2)
    inventory_page.navigate_to_shopping_cart()
    cart_page.check_products(expected_names)


def test_add_product_and_delete_from_cart(login_page, inventory_page, cart_page):
    login_and_check_inventory(login_page, inventory_page)
    product_name = inventory_page.get_product_name(0)
    remaining_name = inventory_page.get_product_name(1)
    inventory_page.add_product_to_cart(0)
    inventory_page.add_product_to_cart(1)
    inventory_page.navigate_to_shopping_cart()
    cart_page.check_products([product_name, remaining_name])
    cart_page.remove_product_from_shopping_cart(product_name)
    cart_page.check_product_absent(product_name)
    cart_page.check_products([remaining_name])
    inventory_page.check_shopping_cart_badge(1)
    cart_page.remove_product_from_shopping_cart(remaining_name)
    cart_page.check_product_absent(remaining_name)
    cart_page.check_products([])
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
    original_products = inventory_page.get_products()
    inventory_page.sort_products(sort_option)
    inventory_page.check_products_sorted(original_products, sort_type, reverse)


@allure.feature("Checkout")
@allure.story("Successful order")
@allure.title("User can successfully complete checkout")
@pytest.mark.smoke
def test_successful_order(login_page, inventory_page, cart_page, checkout_information_page, checkout_complete_page,
                          checkout_overview_page):
    login_and_check_inventory(login_page, inventory_page)
    expected_products = [
        (inventory_page.get_product_name(index),
         Decimal(inventory_page.get_product_price(index).removeprefix("$")))
        for index in (0, 1)
    ]
    for index in (0, 1):
        inventory_page.add_product_to_cart(index)
    inventory_page.check_shopping_cart_badge(2)
    inventory_page.navigate_to_shopping_cart()
    cart_page.click_checkout_button()
    checkout_information_page.fill_information_form("Alex", "Johnson", "02110")
    checkout_information_page.click_continue_button()
    checkout_overview_page.header.check_title_and_page_opened("Checkout: Overview")
    checkout_overview_page.check_order(expected_products)
    checkout_overview_page.click_finish_button()
    checkout_complete_page.check_order_is_successful(SUCCESSFUL_ORDER, COMMENT_FOR_SUCCESSFUL_ORDER)


@pytest.mark.parametrize("first_name, last_name, postal_code, expected_error", [
    pytest.param("", "", "", "Error: First Name is required", id="empty-form"),
    pytest.param("", "Johnson", "02110", "Error: First Name is required", id="empty-first-name"),
    pytest.param("Alex", "", "02110", "Error: Last Name is required", id="empty-last-name"),
    pytest.param("Alex", "Johnson", "", "Error: Postal Code is required", id="empty-postal-code"),
])
def test_checkout_without_data(login_page, inventory_page, cart_page, checkout_information_page,
                               first_name, last_name, postal_code, expected_error):
    login_and_check_inventory(login_page, inventory_page)
    inventory_page.add_product_to_cart(0)
    inventory_page.check_shopping_cart_badge(1)
    inventory_page.navigate_to_shopping_cart()
    cart_page.click_checkout_button()
    checkout_information_page.fill_information_form(first_name, last_name, postal_code)
    checkout_information_page.click_continue_button()
    checkout_information_page.check_form_error_is_displayed()
    checkout_information_page.check_form_error_message(expected_error)
