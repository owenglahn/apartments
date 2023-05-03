from sys import stderr
from selenium import webdriver
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support import expected_conditions as EC
# from python_anticaptcha import AnticaptchaClient
import os
import validators
from config import CHROMEDRIVER_PATH, EVAL_WEB_URL

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(EVAL_WEB_URL)

    query_select = driver.find_element(by=By.ID, value="adresse")
    query_select.click()

    continuer = None
    try:
        continuer = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "Continuer"))
        )
    finally:
        driver.quit()
    continuer.click()

    driver.quit()


if __name__ == "__main__":
    main()