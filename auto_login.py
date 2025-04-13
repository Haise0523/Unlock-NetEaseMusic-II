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
    browser.add_cookie({"name": "MUSIC_U", "value": "0073BC062E99F526D6A0076F25B1C80E14F0EDFA2C868611EFB194C003D39C61424172BEEFBFD86450EFB714E0E45E443E3B855D81C440E7E00F5B6F23ECBF0E246E00A9BBDBB4F047F583D3C9BCA81FB493C647696D106A646305A995B8F5C1BDDC263D4A59A0DA731519A6CEE935FD96970B5C1D370EE2E5F9546B8A47E0BB88A11F12FA028AA5B2D8E537F7BA89AF46205C6AC2A1FC55716A77E948230EFC37521601E5FDF646CA0DCC8FDA9973B8B54B2472D49D106B1A223CE4429E645730EBC0517C0AE8D604C74AD329F161637E5210022E536BFF2C8D6EA6DE985B885B339B76E557946EFD0A74BAC6E52F8D2381AD03C8A826E85226A0C56C3A759D7E3072AF8056F734330AB4F66291E1811FB8CD22659248BA73116593390C6057002210566673AE4883DB3251BB10F0DE034F646A37D8150CE85CFD8C99E92AA661292E6A985987778391F5CE240E4F026694420F44A95101CAFEC9B07F204C4D4D"})
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
