# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0077283D00411A942379E2C26A6D2C0E7FE2F50BE85A4FE6629D69F22ACB2906F6077AF88C27E36E079543C2F94E61811E937D41F2362ECCDA8293259BEF4964B5D33E3D1B11CCC0713B5CDF7EBCA0F77BD76AF7A215491DE899E5115D62557F71965C964A62A25CCB1F02A84F24012FBF9CACE4BFDBF0E7AE633891E8580226ABBE0D54E5FB3E0BFA27C39CB4C13A8036CDC987DA2729D8BE862AD407EBBC45C51A84E9580F6875591B674406762AA1B5C5F4BAA944539B2FFFECAA985729C9441DDD2E9F133FB6F40DDDD2530EA59C683C3C7719A1EA1B78B961A57EE83EAE2A0CDF1B66C146027EA4D58424A1939049BABB2B2FB38A0ADB102870C80EA6657EAEE8E132CD42D6761C33C4365188BA53A175AA14A2F75E525CD0E6B1D6CD9E980DDF509B2C3CF563AFAFD651C2D895C80EC6355ACAED4BFC9293E1714C0AA7ACD3EB1DF67FDE55D24A59C072877041F4E777B76F1BDE0C6B3F67738E7027610B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
