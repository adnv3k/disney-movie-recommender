from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from utils.disneywiki import disney_id


# error css selector: #email__error
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])


class Browser:
    def __init__(self, email=None, password=None, movie=None):
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
        self.email = email
        self.password = password
        self.action = ActionChains(self.driver)
        self.time = time.time()
        self.url = f'https://www.disneyplus.com/movies/wd/{disney_id(movie)}'

    def start(self):
        self.driver.get('https://disneyplus.com')

    def login(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav.nav.pre-sticky > a > span")))
        try:
            self.driver.find_element_by_css_selector('body > header > nav.nav.pre-sticky > a > span').click()
            temp = open('temp.txt', 'r+').readlines()
            self.email = temp[0]
            self.password = temp[1]
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
            self.driver.find_element_by_css_selector("#email").send_keys(self.email)
            self.driver.find_element_by_css_selector("#dssLogin > div:nth-child(3) > button").click()
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
            self.driver.find_element_by_css_selector("#password").send_keys(self.password)
            self.driver.find_element_by_css_selector("#dssLogin > div > button").click()
        except Exception as e:
            print(e)
            self.driver.get_screenshot_as_file(f'errors/{str(round(self.time))}.png')

    def profile(self):
        profile = 'austin'
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#remove-main-padding_index > div > div > section > ul > div:nth-child(2) > div > h3")))
        profile = self.driver.find_element_by_css_selector(f"div[aria-label='{profile}']")
        self.action.move_to_element(profile).click(profile).perform()

    def navigate(self):
        self.driver.get(self.url)
        play_btn = '#details_index > div > article > div.sc-kIWQTW.jsHMGz > div > div.sc-gjAXCV.dEcjHa > button.button.button-play.button-play--default.skipToContentTarget'
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, play_btn)))
        self.driver.find_element(By.CSS_SELECTOR, play_btn).click()
        # make fullscreen
        self.driver.fullscreen_window()

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    b = Browser(movie='Toy Story')
    try:
        b.start()
        b.login()
        b.profile()
        time.sleep(5)
        b.navigate()
    except KeyboardInterrupt:
        b.close()

