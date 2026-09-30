from playwright.sync_api import Page, expect
from pages.components.header import Header


class CheckoutOverviewPage:

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

        self.inventory_item = page.get_by_test_id("inventory-item")
        self.inventory_item_name = page.get_by_test_id("inventory-item-name")
        self.inventory_item_price = page.get_by_test_id("inventory-item-price")
        self.cancel_button = page.get_by_role("button", name = "Cancel")
        self.finish_button = page.get_by_role("button", name = "Finish")

    def click_finish_button(self):
        self.finish_button.click()