import pytest
import requests
from selene import browser, have

from utils.logger import log_request

BASE_URL = "https://demowebshop.tricentis.com"
LOGIN_URL = f"{BASE_URL}/login"
CART_URL = f"{BASE_URL}/cart"

EMAIL = "auto_tester@tester.qa"
PASSWORD = "!234Qwer"

# Сессия для сохранения cookies
session = requests.Session()


# Фикстура для авторизации
@pytest.fixture(scope="session")
def login():
    """Авторизация пользователя перед тестами"""
    login_data = {
        "Email": EMAIL,
        "Password": PASSWORD,
        "RememberMe": False
    }
    response = session.post(LOGIN_URL, data=login_data)
    log_request(response)
    assert response.status_code == 200


@pytest.fixture
def clear_cart():
    """Очистка корзины перед каждым тестом"""
    browser.open(CART_URL)
    items = browser.all(".cart-item-row")
    if items.with_(timeout=2).matching(have.size_greater_than(0)):
        for item in items:
            item.element(".remove-from-cart input").click()
        browser.element(".update-cart-button").click()
        browser.element(".order-summary-content").should(have.text("Your Shopping Cart is empty!"))