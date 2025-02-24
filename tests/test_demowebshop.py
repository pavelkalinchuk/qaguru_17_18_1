import pytest
from allure import step
import allure
from selene import browser

from pages.cart_page import CartPage
from tests.conftest import session

BASE_URL = "https://demowebshop.tricentis.com"

PRODUCTS = [
    {"url": f"{BASE_URL}/addproducttocart/catalog/43/1/1", "name": "Smartphone"},
    {"url": f"{BASE_URL}/addproducttocart/catalog/36/1/1", "name": "Book"},
    {"url": f"{BASE_URL}/addproducttocart/catalog/31/1/1", "name": "Laptop"}
]


def add_product_to_cart(product_url):
    """Добавляет товар в корзину через API"""
    with step("Добавляем товар в корзину"):
        response = session.post(product_url)
        assert response.status_code == 200


def transfer_cookies_to_browser():
    """Передаём куки из API-сессии в браузер"""
    for cookie in session.cookies:
        browser.driver.add_cookie({"name": cookie.name, "value": cookie.value})
    browser.open(BASE_URL)  # Обновляем страницу для применения кук


# Тест с параметризацией
@allure.title("Добавляем товар в корзину, проверям что он добавился, удаляем его из корзины, проверяем что корзина "
              "пуста")
@pytest.mark.parametrize("product", PRODUCTS, ids=[product["name"] for product in PRODUCTS])
def test_add_and_remove_product(login, clear_cart, product):
    """Тест для добавления, проверки и удаления товара из корзины"""
    cart_page = CartPage()

    with step(f"Товар: {product['name']}"):
        add_product_to_cart(product["url"])

        transfer_cookies_to_browser()

        cart_page.check_product_in_cart(product["name"])

        cart_page.remove_product_from_cart()

        cart_page.check_empty_cart()

