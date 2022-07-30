from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


# error css selector: #email__error

class Browser:
    def __init__(self, email, password, profile):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.email = email
        self.password = password
        self.profile = profile
        self.action = ActionChains(self.driver)
        self.time = time.time()

    def start(self):
        self.driver.get('https://disneyplus.com')

    def login(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav.nav.pre-sticky > a > span"))
        )
        try:
            self.driver.find_element_by_css_selector('body > header > nav.nav.pre-sticky > a > span').click()
            temp = open('temp.txt', 'r+').readlines()
            self.email = temp[0]
            self.password = temp[1]

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))
            )
            self.driver.find_element_by_css_selector("#email").send_keys(self.email)
            self.driver.find_element_by_css_selector("#dssLogin > div:nth-child(3) > button").click()

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
            )
            self.driver.find_element_by_css_selector("#password").send_keys(self.password)
            self.driver.find_element_by_css_selector("#dssLogin > div > button").click()

        except Exception as e:
            print(e)
            self.driver.get_screenshot_as_file(f'errors/{str(round(self.time))}.png')

    def profile(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#remove-main-padding_index > div > div > section > ul > div:nth-child(2) > div > h3")))
        prof = self.driver.find_element_by_css_selector(f"div[aria-label='{self.profile}']")
        self.action.move_to_element(prof).click(prof).perform()

