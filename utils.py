from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

def accept_all_cookies(driver):
    try:
        cookie_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "onetrust-button-group-parent"))
        )

        if cookie_div:
            print("-- Cookie accept div open")
            accept_button = cookie_div.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_button.click()
            print("-- Clicked 'Accept All' button inside shadow DOM.")
        else:
            print("-- Shadow DOM is not open.")
        
    except Exception:
        print("--No window to accept: Shadow DOM or button not found.")
        
def sleep(min_time=0.5, max_time=2.0):
    sleeptime = random.uniform(min_time, max_time)
    time.sleep(sleeptime)  
        
