from collections import Counter
from decimal import Decimal

from playwright.sync_api import Page, expect
from pages.components.header import Header


class InventoryPage:

    def __init__(self, page: Page):
        self.header = Header(page)

        self.inventory_item = page.get_by_test_id("inventory-item")
        self.inventory_item_name = page.get_by_test_id("inventory-item-name")
        self.inventory_item_price = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_role("combobox", name="Sort products")

    def get_product(self, product_index: int):
        return self.inventory_item.nth(product_index)

    def get_product_name(self, product_index: int) -> str:
        product = self.get_product(product_index)
        return product.get_by_test_id("inventory-item-name").inner_text()

    def get_product_price(self, product_index: int) -> str:
        product = self.get_product(product_index)
        return product.get_by_test_id("inventory-item-price").inner_text()

    def add_product_to_cart(self, product_index: int):
        product = self.get_product(product_index)
        product.get_by_role("button", name="Add to cart").click()

    def navigate_to_shopping_cart(self):
        self.header.cart.click()

    def check_shopping_cart_badge(self, expected_amount: int):
        expect(self.header.shopping_cart_badge).to_have_text(str(expected_amount))

    def check_shopping_cart_empty(self):
        expect(self.header.empty_shopping_cart).to_be_visible()

    def sort_products(self, option: str):
        self.sort_dropdown.select_option(option)

    def get_products(self) -> list[tuple[str, Decimal]]:
        return [
            (self.get_product_name(index), Decimal(self.get_product_price(index).removeprefix("$")))
            for index in range(self.inventory_item.count())
        ]

    def check_products_sorted(self, original_products, sort_type: str, reverse: bool):
        assert len(original_products) > 1, "Sorting requires at least two products"
        key_index = 0 if sort_type == "name" else 1
        expected_values = sorted(
            (product[key_index] for product in original_products), reverse=reverse
        )
        expect(self.inventory_item).to_have_count(len(original_products))
        if sort_type == "name":
            expect(self.inventory_item_name).to_have_text(expected_values)
        else:
            expect(self.inventory_item_price).to_have_text(
                [f"${price:.2f}" for price in expected_values]
            )
        actual_products = self.get_products()
        assert Counter(actual_products) == Counter(original_products), (
            f"Catalog changed during sorting: before={original_products}, after={actual_products}"
        )
