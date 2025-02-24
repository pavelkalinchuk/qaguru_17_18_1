from selene import browser, have
from allure_commons.types import AttachmentType
import allure

BASE_URL = "https://demowebshop.tricentis.com"


class CartPage:
    """Класс для работы с корзиной"""

    def check_product_in_cart(self, product_name):
        """Проверяем, что товар добавлен в корзину"""
        with allure.step(f"Проверяем, что товар '{product_name}' добавлен в корзину"):
            browser.open(f"{BASE_URL}/cart")
            allure.attach(browser.driver.get_screenshot_as_png(), name=f"Cart with {product_name}",
                          attachment_type=AttachmentType.PNG)
            browser.all(".cart-item-row").should(have.size(1))

    def remove_product_from_cart(self):
        """Удаляем товар из корзины"""
        with allure.step("Удаляем товар из корзины"):
            remove_button = browser.element(".remove-from-cart input")
            remove_button.click()
            browser.element(".update-cart-button").click()

    def check_empty_cart(self):
        """Проверяем, что корзина пуста"""
        with allure.step("Проверяем, что корзина пуста"):
            browser.element(".order-summary-content").should(have.text("Your Shopping Cart is empty!"))
            allure.attach(browser.driver.get_screenshot_as_png(), name="Empty Cart", attachment_type=AttachmentType.PNG)
