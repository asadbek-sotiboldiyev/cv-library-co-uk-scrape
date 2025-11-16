from selenium.webdriver.common.by import By
import time

def get_pagination_numbers(driver):
    pagination_items = driver.find_elements(By.CSS_SELECTOR, "ol.pagination__list a.pagination__item")
    return [int(item.text.strip()) for item in pagination_items]

def go_to_next_page(driver):
    next_button = driver.find_element(By.CLASS_NAME, 'pagination__next')
    next_button.click()
    time.sleep(10)