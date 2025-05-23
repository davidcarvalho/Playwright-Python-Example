import allure
import pytest
from playwright.sync_api import Page, expect

from src.enums.User import User
from src.pages.login_page import LoginPage


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.login_page = LoginPage(page)

    @pytest.mark.devRun
    @allure.title("Login with valid credentials test")
    def test_valid_login(self, base_url, page: Page) -> None:
        self.login_page.login(User.STANDARD_USER, "secret_sauce")
        expect(page).to_have_url(f"{base_url}inventory.html")

    @pytest.mark.parametrize(
        "username, password, expected_error",
        [
            (
                User.STANDARD_USER,
                "secret_sauce1",
                "Epic sadface: Username and password do not match any user in this service",
            ),
            (
                User.LOCKED_OUT_USER,
                "secret_sauce",
                "Epic sadface: Sorry, this user has been locked out.",
            ),
        ],
        ids=["invalid_password", "locked_user"],
    )
    @allure.title("Login with invalid credentials test")
    def test_login_error(
        self, page: Page, username: str, password: str, expected_error: str
    ) -> None:
        self.login_page.login(username, password)
        expect(self.login_page.error_message).to_have_text(expected_error)
