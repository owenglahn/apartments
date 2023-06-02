from fake_useragent import UserAgent
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from config import CHROMEDRIVER_PATH, EVAL_WEB_URL, OUTPUT_FILE 
from selenium.common.exceptions import NoSuchElementException

from config import CHROMEDRIVER_PATH

class Scraper:
    def __init__(self):
        self.ua = UserAgent()

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(f'user-agent={self.ua.random}')

        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)

    def change_agent(self):
        self.quit()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument(f'user-agent={self.ua.chrome}')
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)

    def collect_names(self, lot_num: str):
        self.driver.get(EVAL_WEB_URL)
        query_select = self.driver.find_element(by=By.ID, value="lot")
        query_select.click()

        continuer = self.driver.find_element(by=By.XPATH, value='//*[@id="type_recherche"]/button')
        continuer.click()
        time.sleep(.5)

        lotnum_entry = self.driver.find_element(by=By.ID, value="noLotRenove")
        lotnum_entry.send_keys(lot_num)
        time.sleep(.5)

        try:
            captcha_iframe = self.driver.find_element(by=By.XPATH, value='//*[@id="adressForm"]/div/div[2]/div/div/div/div/div/iframe')
            self.driver.switch_to.frame(captcha_iframe)
            recaptcha = self.driver.find_element(by=By.CLASS_NAME, value="recaptcha-checkbox-border")
            recaptcha.click()
            self.driver.switch_to.default_content()
        except NoSuchElementException:
            # self.change_agent()
            return False

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@value="Rechercher"]'))).click()

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "index")))
        radio_buttons = self.driver.find_elements(by=By.NAME, value="index")
        for button in radio_buttons:
            pid = os.fork()
            output_file = open(OUTPUT_FILE, "w")
            if pid == 0:
                button.click()
                soumettre = self.driver.find_element(by=By.XPATH, value='//*[@id="adressForm"]/div/div[2]/button')
                soumettre.click()
                name = self.driver.find_element(by=By.XPATH, value='//*[@id="section-2"]/table/tbody/tr[1]/th')
                output_file.write(name.text)
            output_file.close()

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="play-zone"]/div/div[1]/div[1]/div/a'))).click()
        return True

    def search_contact(self):
        return
    
    def quit(self):
        self.driver.quit()
