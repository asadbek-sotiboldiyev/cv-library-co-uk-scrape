from selenium.webdriver.common.by import By
from utils import sleep
from selenium.webdriver.common.keys import Keys

def search_keyword(driver, keyword: str):
    search_input = driver.find_element(By.CLASS_NAME, "search-nav__input")
    search_input.clear()
    search_input.send_keys(keyword, Keys.ENTER)
    sleep(1.0, 2.0)
    
