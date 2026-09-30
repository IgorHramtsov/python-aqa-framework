from playwright.sync_api import Page, expect
from pages.components.header import Header


class CartPage:

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)


        self.item = page.get_by_test_id("inventory-item")
        self.item_quantity = page.get_by_test_id("item-quantity")
        self.inventory_item_name = page.get_by_test_id("inventory-item-name")
        self.inventory_item_price = page.get_by_test_id("inventory-item-price")
        # self.shopping_cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.remove_item = page.get_by_role("button", name = "Remove")
        self.continue_shopping = page.get_by_role("button", name = "Continue Shopping")
        self.checkout_button = page.get_by_role("button", name = "Checkout")

    def get_shopping_cart_badge_amount(self) -> str:
        return self.header.shopping_cart_badge.inner_text()

    def get_product(self, product_index: int):
        return self.item.nth(product_index)

    def get_product_quantity(self, product_index: int):
        return self.item_quantity.nth(product_index).inner_text()

    def get_product_name(self, product_index: int):
        return self.inventory_item_name.nth(product_index).inner_text()

    def get_product_price(self, product_index: int):
        return self.inventory_item_price.nth(product_index).inner_text()

    def remove_product_from_shopping_cart(self):
        self.remove_item.click()

    def back_to_inventory_page(self):
        self.continue_shopping.click()

    def click_checkout_button(self):
        self.checkout_button.click()


