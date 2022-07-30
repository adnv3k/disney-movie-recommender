from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


# error css selector: #email__error

driver = webdriver.Chrome('browser/chromedriver.exe')
action = ActionChains(driver)
driver.get('https://disneyplus.com')
t = time.time()

# do login process
try:
    # set up explicit wait time and search for login button
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body > header > nav.nav.pre-sticky > a > span"))
    )
    driver.find_element_by_css_selector('body > header > nav.nav.pre-sticky > a > span').click()
    temp = open('temp.txt', 'r+').readlines()
    email = temp[0]
    pw = temp[1]
    profile = 'Profile'

    email_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))
    )
    driver.find_element_by_css_selector("#email").send_keys(email)
    driver.find_element_by_css_selector("#dssLogin > div:nth-child(3) > button").click()

    pw_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
    )
    driver.find_element_by_css_selector("#password").send_keys(pw)
    driver.find_element_by_css_selector("#dssLogin > div > button").click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#remove-main-padding_index > div > div > section > ul > div:nth-child(2) > div > h3"))
    )
    prof = driver.find_element_by_css_selector(f"div[aria-label='{profile}']")
    action.move_to_element(prof).click(prof).perform()

except Exception as e:
    print(e)
    driver.get_screenshot_as_file(f'errors/{str(round(t))}.png')
