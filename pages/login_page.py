from playwright.sync_api import Page, expect
from config.config import BASE_UI_URL


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def open_login_page(self):
        self.page.goto(BASE_UI_URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def check_error_message(self, expected_message: str):
        expect(self.error_message).to_have_text(expected_message)

