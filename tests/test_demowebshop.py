import pytest
from allure import step
from selene import browser, have
from allure_commons.types import AttachmentType
import allure

from tests.conftest import session

# Конфигурация
BASE_URL = "https://demowebshop.tricentis.com"

# Список товаров для добавления в корзину
PRODUCTS = [
    {"url": f"{BASE_URL}/addproducttocart/catalog/43/1/1", "name": "Smartphone"},
    {"url": f"{BASE_URL}/addproducttocart/catalog/36/1/1", "name": "Book"},
    {"url": f"{BASE_URL}/addproducttocart/catalog/31/1/1", "name": "Laptop"}
]


def add_product_to_cart(product_url):
    """Добавляет товар в корзину через API."""
    response = session.post(product_url)
    assert response.status_code == 200


def transfer_cookies_to_browser():
    """Передает куки из API-сессии в браузер."""
    with step("Передаем куки из API-сессии в браузер"):
        for cookie in session.cookies:
            browser.driver.add_cookie({"name": cookie.name, "value": cookie.value})
        browser.open(BASE_URL)  # Обновляем страницу для применения кук


def check_product_in_cart(product_name):
    """Проверяет, что товар добавлен в корзину."""
    with step(f"Проверяем, что товар '{product_name}' добавлен в корзину"):
        browser.open(f"{BASE_URL}/cart")
        allure.attach(browser.driver.get_screenshot_as_png(), name=f"Cart with {product_name}", attachment_type=AttachmentType.PNG)
        browser.all(".cart-item-row").should(have.size(1))


def remove_product_from_cart():
    """Удаляет товар из корзины."""
    with step("Удаляем товар из корзины"):
        remove_button = browser.element(".remove-from-cart input")
        remove_button.click()
        browser.element(".update-cart-button").click()


def check_empty_cart():
    """Проверяет, что корзина пуста."""
    with step("Проверяем, что корзина пуста"):
        browser.element(".order-summary-content").should(have.text("Your Shopping Cart is empty!"))
        allure.attach(browser.driver.get_screenshot_as_png(), name="Empty Cart", attachment_type=AttachmentType.PNG)


@allure.title("Добавляем товар в корзину, проверяем что он в корзине, удаляем из корзины, проверяем что корзина пуста")
@pytest.mark.parametrize("product", PRODUCTS, ids=[product["name"] for product in PRODUCTS])
def test_add_and_remove_product(login, clear_cart, product):
    """Тест для добавления, проверки и удаления товара из корзины."""
    with step(f"Обрабатываем товар: {product['name']}"):
        # Добавление товара в корзину
        add_product_to_cart(product["url"])

        # Передача кук из API-сессии в браузер
        transfer_cookies_to_browser()

        # Проверка, что товар добавлен
        check_product_in_cart(product["name"])

        # Удаление товара из корзины
        remove_product_from_cart()

        # Проверка, что корзина пуста
        check_empty_cart()


# # Запуск тестов
# if __name__ == "__main__":
#     pytest.main(["-v", "--alluredir=./allure-results"])