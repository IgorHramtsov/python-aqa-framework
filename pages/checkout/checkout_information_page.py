from playwright.sync_api import Page, expect
from pages.components.header import Header


class CheckoutInformationPage:

    def __init__(self, page: Page):
        self.page = page
        self.header = Header(page)

        self.first_name_input = page.get_by_test_id("firstName")
        self.last_name_input = page.get_by_test_id("lastName")
        self.postal_code_input = page.get_by_test_id("postalCode")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.error_message = page.get_by_test_id("error")
        self.error_button = page.get_by_test_id("error-button")

    def fill_information_form(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def click_continue_button(self):
        self.continue_button.click()

    def check_form_error_is_displayed(self):
        expect(self.error_message).to_be_visible()
        expect(self.error_button).to_be_visible()

    def check_form_error_message(self, expected_message):
        expect(self.error_message).to_have_text(expected_message)
