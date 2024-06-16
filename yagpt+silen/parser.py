from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time



# Настройка веб-драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Открытие веб-страницы
    url = ""  # тест ссылка Замените на нужную ссылку
    driver.get(url)

    # Ожидание загрузки страницы (по необходимости можно увеличить время)
    time.sleep(3)

    # Поиск элемента и получение его текста
    # Получение текста всего тела страницы
    classes = "uiArticleBlockText_i9h2o text-style-body-1 c-text block_fefJj" # для 72 ру чтобы брать текст инфу от туда
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f".{classes.replace(' ', '.')}"))
    )
    elements = driver.find_elements(By.CSS_SELECTOR, f".{classes.replace(' ', '.')}")

    with open("page1.txt", "w", encoding="utf-8") as file:
        for element in elements:
            text = element.text
            file.write(text + "\n\n")  # Запись текста в файл с разделением


finally:
    # Закрытие драйвера
    driver.quit()
