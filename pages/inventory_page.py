from playwright.sync_api import Page, expect
from pages.components.header import Header


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

        self.inventory_list = page.get_by_test_id("inventory-list")
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

    def get_shopping_cart_badge_amount(self) -> str:
        return self.header.shopping_cart_badge.inner_text()

    def navigate_to_shopping_cart(self):
        self.header.cart.click()

    def check_shopping_cart_badge(self, expected_amount: int):
        expect(self.header.shopping_cart_badge).to_have_text(str(expected_amount))

    def check_shopping_cart_empty(self):
        expect(self.header.empty_shopping_cart).to_be_visible()

    def sort_products(self, option: str):
        self.sort_dropdown.select_option(option)

    def check_products_sorted_by_name(self, reverse: bool = False):
        actual_names = self.inventory_item_name.all_inner_texts()
        expected_names = sorted(actual_names, reverse=reverse)

        assert actual_names == expected_names

    def check_products_sorted_by_price(self, reverse: bool = False):
        price_texts = self.inventory_item_price.all_inner_texts()

        actual_prices = [
            float(price.replace("$", ""))
            for price in price_texts
        ]

        expected_prices = sorted(actual_prices, reverse=reverse)
        assert actual_prices == expected_prices
