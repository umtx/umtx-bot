from flask import Flask, request, jsonify
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from umtis.fetch import main as fetch_main
from umtis.seleniumpro.local_storage import LocalStorage
import random
import undetected_chromedriver as uc
import requests
import time
import os
import json
from concurrent import futures
from umtis import log

logger = log.setup_logging("SIS")

app = Flask(__name__)

# Constants
LOGIN_TIMEOUT = 10
WAIT_SHORT = 0.3
WAIT_MEDIUM = 0.5
WAIT_LONG = 3

def sleep_and_wait(seconds):
    time.sleep(seconds)
    
def wait_and_click(driver, xpath_value, timeout=LOGIN_TIMEOUT):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath_value))).click()

def wait_and_send_keys(driver, xpath_value, value, timeout=LOGIN_TIMEOUT):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath_value))).send_keys(value)

def find_element(driver, xpath_value):
    return len(driver.find_elements(By.XPATH, xpath_value)) > 0

def click_if_found(driver, xpath_value):
    logger.info(f"Checking if element exists: {xpath_value}")
    sleep_and_wait(WAIT_SHORT)
    if find_element(driver, xpath_value):
        logger.info(f"Clicking on element: {xpath_value}")
        driver.find_element(By.XPATH, xpath_value).click()

def login_successful(driver):
    return EC.url_contains("office.com")(driver)

def fetch_access_token(driver):
    lcs = LocalStorage(driver)
    user = json.loads(lcs.get("sis-auth-react"))
    uid = user['user']['uid']
    pid = user['user']['id']
    access_token = user['token']
    
    return access_token


def perform_login(user_profile, request_id):
    options = uc.ChromeOptions()
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('-no-first-run')
    options.add_argument('-password-store=basic')
    options.add_argument('-use-mock-keychain')
    options.add_argument('-no-default-browser-check')
    options.add_argument('-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions')
    options.add_argument('-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage')
    options.add_argument('-deny-permission-prompts')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--dns-prefetch-disable')  # Disable DNS prefetching
    options.add_argument('--dns-server=8.8.8.8')

    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--clear-data")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    logger.info(f"[{request_id}] Initiating login process")
    
    driver = uc.Chrome(options=options, headless=False)
    driver.get("https://login.microsoftonline.com/")

    logger.info(f"[{request_id}] Waiting for login page to load")
    wait_and_send_keys(driver, "//input[@id='i0116']", user_profile['username'])
    logger.info(f"[{request_id}] Filled username")

    wait_and_click(driver, '//input[@id="idSIButton9"]', request_id)

    if find_element(driver, '//div[@id="usernameError"]'):
        driver.close()
        logger.error(f"[{request_id}] Login failed: Wrong Username")
        return {"error": True, "msg": "WRONG_USERNAME"}

    wait_and_send_keys(driver, '//input[@id="i0118"]', user_profile['password'])
    logger.info(f"[{request_id}] Filled password")

    wait_and_click(driver, '//input[@id="idSIButton9"]', request_id)

    if find_element(driver, '//div[@id="passwordError"]'):
        driver.close()
        logger.error(f"[{request_id}] Login failed: Wrong password")
        return {"error": True, "msg": "WRONG_PASSWORD"}

    logger.info(f"[{request_id}] Confirming login")

    click_if_found(driver, '//input[@id="idSIButton9"]')
    WebDriverWait(driver, LOGIN_TIMEOUT).until(login_successful)
    logger.info(f"[{request_id}] SIS Login")


    consent_response = requests.get("https://apisis.umt.edu.vn/api/v1.0/auth2/authorize?role=STUDENT")
    consent_url = consent_response.text.replace('user.read%20offline_access%20openid%20profile', 'openid')

    driver.get(consent_url)
    logger.info(f"[{request_id}] Microsoft consent page loaded")
    WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="row title ext-title"]')))
    user_element_exists = find_element(driver, f"//div[@class='table'][@tabindex='0'][@role='button'][@data-test-id='{user_profile['username']}']")
    if not user_element_exists:
        logger.warning(f"[{request_id}] Login failed. Try again")
        driver.close()
        return {"error": True, "msg": "UNKNOWN_ERROR"}
    else:
        logger.info(f"[{request_id}] User element found, clicking login")
        wait_and_click(driver, f"//div[@class='table'][@tabindex='0'][@role='button'][@data-test-id='{user_profile['username']}']", request_id)
        logger.info(f"[{request_id}] Login click success")
        WebDriverWait(driver, LOGIN_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="row title ext-title"]')))

        wait_and_click(driver, '//input[@id="idSIButton9"]')

    logger.info(f"[{request_id}] Waiting for login success")
    WebDriverWait(driver, 50).until(EC.url_contains("https://sis.umt.edu.vn/my-schedule"))
    logger.info("Load success! Fetch token! Last step")
    # Rest of the login process here
    access_token = fetch_access_token(driver)

    driver.close()

    if len(access_token) > 0:
        return {"error": False, "token": access_token, "message": "SUCCESS"}
    else:
        return {"error": True, "message": "UNKNOWN_ERROR"}


@app.route('/')
def ping():
    return 'pong'

@app.route('/login', methods=['POST'])
def browser():
    nid = random.randint(1000000, 9999999)
    logger.info(f'[{nid}] New request')

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        user_profile = request.json
    else:
        user_profile = {
            "username": request.args.get("username"),
            "password": request.args.get("password")
        }

    try:
        return_data = perform_login(user_profile, nid)
    except Exception as e:
        logger.error(e)
        return {"error": True, "message": "UNKNOWN_ERROR"}

    return jsonify(return_data)

if __name__ == '__main__':
    app.run(threaded=False, processes=8, host="0.0.0.0", port=os.getenv("PORT"))
