from playwright.sync_api import Page, expect


class CartPage:

    def __init__(self, page: Page):
        self.page = page

        self.item = page.get_by_test_id("inventory-item")
        self.inventory_item_name = page.get_by_test_id("inventory-item-name")
        self.inventory_item_price = page.get_by_test_id("inventory-item-price")
        self.continue_shopping = page.get_by_role("button", name="Continue Shopping")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def get_product_price(self, product_index: int):
        return self.inventory_item_price.nth(product_index).inner_text()

    def check_products(self, expected_names: list[str]):
        expect(self.inventory_item_name).to_have_text(expected_names)

    def remove_product_from_shopping_cart(self, product_name: str):
        product = self.item.filter(
            has=self.page.get_by_test_id("inventory-item-name").get_by_text(product_name, exact=True)
        )
        product.get_by_role("button", name="Remove", exact=True).click()

    def check_product_absent(self, product_name: str):
        expect(self.inventory_item_name.get_by_text(product_name, exact=True)).to_have_count(0)

    def back_to_inventory_page(self):
        self.continue_shopping.click()

    def click_checkout_button(self):
        self.checkout_button.click()


