from playwright.sync_api import Page, expect


class Header:

    def __init__(self, page: Page):
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logo = page.get_by_text("Swag Labs", exact=True)
        self.cart = page.get_by_test_id("shopping-cart-link")
        self.title = page.get_by_test_id("title")
        self.shopping_cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.empty_shopping_cart = page.get_by_role("button", name="Cart, empty")

    def check_title_and_page_opened(self, expected_title: str):
        expect(self.title).to_have_text(expected_title)
        expect(self.logo).to_have_text("Swag Labs")
        expect(self.cart).to_be_visible()
        expect(self.menu_button).to_be_visible()
