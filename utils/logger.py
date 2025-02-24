import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    handlers=[logging.StreamHandler()]  # Вывод в консоль
)
logger = logging.getLogger(__name__)


def log_request(response):
    """Логируем информацию о запросе и ответе"""
    # Логируем запрос
    logger.info(f"Request URL: {response.request.url}")
    logger.info(f"Request Method: {response.request.method}")
    logger.info(f"Request Headers: {response.request.headers}")
    # if response.request.body:
    #     logger.info(f"Request Body: {response.request.body}")

    # Логируем ответ
    logger.info(f"Response Status Code: {response.status_code}")
    logger.info(f"Response Headers: {response.headers}")
    # logger.info(f"Response Body: {response.text}")