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
    browser.add_cookie({"name": "MUSIC_U", "value": "003A57417EFFABD7EF38F26A651382E99F68EA643B8426EF54CCDFC2A5E149508D302C4776F2499E346A0B8B9F8BFA3F800C9D2A27D8B397B24075DECE72400B6559770F959B32CD4ED03E19C5C3F3F77B098094742E8C091928E75F76EFA010297B108F475C72657F43BA4C2914E7160DBF8651AA3C70EBC10FE2061714023A8B19FBE48E5C6796B2F3ACA1F647D822BAABA2B260AAD0CCC3AC629DEDCC85D2B1DC7C8B75C378EF0735386797F3AD0BCECA30C93526FBDB84D5AE8BDD584E2F9C8986A47F3B2C08F591117CA5F2D4CFBBCA8077DAA05EC452F844E41AE4B5CE4082DF9768A4B21A70B0AF52DD72A60D118BFFC791F5554D73289455AF177EBE39D9DEE2B865235DDBE6B6F3E902329EF5636F11F26AB540F49803DAB1F80CA26A9E16759C1303C80DEA080C7CDF603646BAE36754C6525D9C9FEE6800C042E84AF3EF341CABFD39726BF97888626225ED399DAB5D90C187088D21ACFF0D963333"})
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
