from data.constants import STANDARD_USER, PASSWORD


def login_and_check_inventory(login_page, inventory_page):
    login_page.open_login_page()
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page.header.check_title_and_page_opened("Products")