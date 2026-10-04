from playwright.sync_api import Page, expect


class CheckoutCompletePage:

    def __init__(self, page: Page):
        self.complete_thanks = page.get_by_test_id("complete-header")
        self.complete_comment = page.get_by_test_id("complete-text")
        self.back_home_button = page.get_by_role("button", name="Back Home")
        self.generate_pdf_order_button = page.get_by_role("button", name="Generate PDF Order")


    def check_order_is_successful(self, expected_thanks: str, expected_comment: str):
        expect(self.complete_thanks).to_have_text(expected_thanks)
        expect(self.complete_comment).to_have_text(expected_comment)
        expect(self.back_home_button).to_be_visible()
        expect(self.generate_pdf_order_button).to_be_visible()
