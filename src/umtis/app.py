from flask import Flask, render_template, request
import json
import time
import os
import undetected_chromedriver as uc

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from concurrent import futures

from umtis.fetch import main as fetch_main
from umtis.seleniumpro.local_storage import LocalStorage
import random
from umtis import log

logger = log.setup_logging("SIS")

app = Flask(__name__)


def fill_input_xpath(driver: webdriver, xpath_value: str, value: str):
    sleep_and_wait(0.1)
    ignored_exceptions = (StaleElementReferenceException)
    my_elements = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.presence_of_element_located((By.XPATH, xpath_value)))

    while len(driver.find_elements(By.XPATH, xpath_value)) < 1:
        logger.warn('Wait')

        sleep_and_wait(0.1)
    if ((not driver.find_elements(By.XPATH, xpath_value)[0].is_displayed()) or (not driver.find_elements(By.XPATH, xpath_value)[0].is_enabled())):
        sleep_and_wait(0.1)

        
        return fill_input_xpath(driver, xpath_value, value)

    else:
        sleep_and_wait(0.1)
        driver.find_elements(By.XPATH, xpath_value)[0].send_keys(value)


def click_button_xpath(driver: webdriver, xpath_value: str):
    sleep_and_wait(0.1)
    ignored_exceptions = (StaleElementReferenceException)
    my_elements = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.element_to_be_clickable((By.XPATH, xpath_value)))
    while len(driver.find_elements(By.XPATH, xpath_value)) < 1:
        logger.warn('Wait')
        sleep_and_wait(0.1)
    
    if ((not driver.find_elements(By.XPATH, xpath_value)[0].is_displayed()) or (not driver.find_elements(By.XPATH, xpath_value)[0].is_enabled())):
        sleep_and_wait(0.1)
        return click_button_xpath(driver, xpath_value)

    else:
        sleep_and_wait(0.1)

        driver.find_elements(By.XPATH, xpath_value)[0].click()


def find_exist_xpath(driver: webdriver, xpath_value: str):
    sleep_and_wait(0.1)

    
    if len(driver.find_elements(By.XPATH, xpath_value)) < 1:
        sleep_and_wait(0.2)

    return len(driver.find_elements(By.XPATH, xpath_value))


def sleep_and_wait(seconds: int):
    time.sleep(seconds)


def get_random_string(length):
    
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    
    return result_str


@app.route('/')
def ping():
    return 'pong'


def perfomance_login(user_profile):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--no-sandbox')
    
    chrome_options.add_argument("--headless")

    driver = uc.Chrome(options=chrome_options, seleniumwire_options={
    'mitm_websocket': False,

        'verify_ssl': False,
        'ssl_cert_verify': False
    })
    logger.info("Go to https://sis.umt.edu.vn/")
    driver.get('https://sis.umt.edu.vn/')
    
    click_button_xpath(driver, "//span[@class='menu-icon d-block']")
    sleep_and_wait(0.5)
    fill_input_xpath(driver, "//input[@id='i0116']", user_profile['username'])
    

    
    click_button_xpath(driver, '//input[@id="idSIButton9"]')

    is_failed = find_exist_xpath(driver, '//div[@id="usernameError"]')
    if is_failed > 0:
        logger.error("Login failed: Wrong Username")

        driver.close()
        return {"error": True, "msg": "WRONG_USERNAME"}

        
    logger.info("Input email")
    

    fill_input_xpath(driver, '//input[@id="i0118"]', user_profile['password'])

    logger.info("Input password")
    
    click_button_xpath(driver, '//input[@id="idSIButton9"]')

    
    

    logger.info("Login")
    is_failed = find_exist_xpath(driver, '//div[@id="passwordError"]')
    if is_failed > 0:
        logger.error("Login failed: Wrong password")
        driver.close()

        return {"error": True, "msg": "WRONG_PASSWORD"}
        
    
    
    click_button_xpath(driver, '//input[@id="idSIButton9"]')

    ignored_exceptions = (StaleElementReferenceException)
    my_elements = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.url_to_be("https://sis.umt.edu.vn/my-schedule"))

    logger.info("Done fetching TOKEN")

    lcs = LocalStorage(driver)
    user = json.loads(lcs.get("sis-auth-react"))
    uid = user['user']['uid']
    pid = user['user']['id']

    access_token = user['token']

    
    if len(access_token) > 0:
        print({"token":access_token,  "suid": uid})
        return {"error": False, "token": access_token, "message": "SUCCESS", "suid": uid, 'puid': pid}
    else:
        return {"error": True, "message": "UNKNOWN_ERROR"}


@app.route('/login', methods=['POST'])
def browser():
    
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        user_profile = request.json
    else:
        user_profile = {username: request.args.get(
            "username"), password: request.args.get("password")}
    try:
        return_data = perfomance_login(user_profile)
    except Exception as e:
        return {"error": True, "message": "UNKNOWN_ERROR"}
    return return_data
    
    


if __name__ == '__main__':
    from waitress import serve

    app.run(threaded=False, processes=8, host="0.0.0.0", port=os.getenv("PORT"))





