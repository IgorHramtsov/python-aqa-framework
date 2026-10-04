from decimal import Decimal, ROUND_HALF_UP

from playwright.sync_api import Page, expect
from pages.components.header import Header


class CheckoutOverviewPage:

    def __init__(self, page: Page):
        self.header = Header(page)

        self.inventory_item = page.get_by_test_id("inventory-item")
        self.inventory_item_name = page.get_by_test_id("inventory-item-name")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_role("button", name="Finish")

    def check_order(self, expected_products: list[tuple[str, Decimal]]):
        expect(self.inventory_item).to_have_count(len(expected_products))
        expect(self.inventory_item_name).to_have_text([name for name, _ in expected_products])
        for index, (_, price) in enumerate(expected_products):
            item = self.inventory_item.nth(index)
            expect(item.get_by_test_id("item-quantity")).to_have_text("1")
            expect(item.get_by_test_id("inventory-item-price")).to_have_text(f"${price:.2f}")

        subtotal = sum((price for _, price in expected_products), Decimal("0.00"))
        # Sauce Demo applies an 8% sales tax, rounded to cents.
        tax = (subtotal * Decimal("0.08")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        expect(self.subtotal).to_have_text(f"Item total: ${subtotal:.2f}")
        expect(self.tax).to_have_text(f"Tax: ${tax:.2f}")
        expect(self.total).to_have_text(f"Total: ${subtotal + tax:.2f}")

    def click_finish_button(self):
        self.finish_button.click()
