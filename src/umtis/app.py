from flask import Flask, render_template, request
import json
import time
import os
import random
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


def fill_input_xpath(driver: webdriver, xpath_value: str, value: str, ):
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath_value))).send_keys(value)



def click_button_xpath(driver: webdriver, xpath_value: str, id=-1):
    WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath_value))).click()


def soft_click_button_xpath(driver: webdriver, xpath_value: str, id=-1):
    WebDriverWait(driver, 4).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath_value))).click()

def click_if_found(driver: webdriver, xpath_value: str):
    if len(driver.find_elements(By.XPATH, xpath_value)) > 0:
        driver.find_element(By.XPATH, xpath_value).click()
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


def perfomance_login(user_profile, id):
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
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--clear-data")
    options.add_argument("--incognito")

    options.add_argument("--disable-blink-features=AutomationControlled")

    logger.info(f"[{id}] Fire up")
    driver = uc.Chrome(options=options, headless=False)
    driver.get("https://office.com/login")
    logger.info(f"[{id}] Go to https://sis.umt.edu.vn/")

    # driver.get('https://sis.umt.edu.vn/')
    
    # click_button_xpath(driver, "//span[@class='menu-icon d-block']", id)
    # sleep_and_wait(0.3)
    fill_input_xpath(driver, "//input[@id='i0116']", user_profile['username'])
    
    # driver.get_screenshot_as_file("a3.png")


    click_button_xpath(driver, '//input[@id="idSIButton9"]', id)

    is_failed = find_exist_xpath(driver, '//div[@id="usernameError"]')
    if is_failed > 0:
        logger.error(f"[{id}] Login failed: Wrong Username")

        driver.close()
        return {"error": True, "msg": "WRONG_USERNAME"}

        
    logger.info(f"[{id}] Not-error at Input email")
    

    fill_input_xpath(driver, '//input[@id="i0118"]', user_profile['password'])

    logger.info(f"[{id}] Input password done")
    # driver.get_screenshot_as_file("a4.png")

    click_button_xpath(driver, '//input[@id="idSIButton9"]', id)

    
    

    logger.info(f"[{id}] Login")

    is_failed = find_exist_xpath(driver, '//div[@id="passwordError"]')
    if is_failed > 0:
        logger.error(f"[{id}] Login failed: Wrong password")
        driver.close()

        return {"error": True, "msg": "WRONG_PASSWORD"}
        
    logger.info(f"[{id}] Password success")
    driver.get_screenshot_as_file(f"out/{id}-c1.png")


    sleep_and_wait(0.5)
    click_if_found(driver, '//input[@id="idSIButton9"]')
    driver.get_screenshot_as_file(f"out/{id}-c3.png")
    logger.info(f"[{id}] Click success")
    sleep_and_wait(1)
    driver.get_screenshot_as_file(f"out/{id}-c5.png")
    WebDriverWait(driver, 20).until(expected_conditions.url_contains("https://www.office.com/?auth=2"))

    
    driver.get('https://sis.umt.edu.vn/login')
    
    click_button_xpath(driver, "//span[@class='menu-icon d-block']", id)
    sleep_and_wait(0.3)
    WebDriverWait(driver, 20).until(expected_conditions.url_contains("microsoftonline.com"))

    element = find_exist_xpath(driver, f"//div[@class='table'][@tabindex='0'][@role='button'][@data-test-id='{user_profile['username']}']")
    if (element == 0):
        logger.warn(f"[{id} Login failed. Try again")
        driver.close()
        return {"error": True, "msg": "UNKNOWN_ERROR"}
    else:
        logger.info(f"[{id}] Login click")
        click_button_xpath(driver, f"//div[@class='table'][@tabindex='0'][@role='button'][@data-test-id='{user_profile['username']}']", id)
        click_button_xpath(driver, '//input[@id="idSIButton9"]', id)
    WebDriverWait(driver, 5).until(expected_conditions.url_contains("https://sis.umt.edu.vn/my-schedule"))

    logger.info(f"[{id}] Done fetching token")
    driver.get_screenshot_as_file(f"out/{id}-c8.png")

    lcs = LocalStorage(driver)
    user = json.loads(lcs.get("sis-auth-react"))
    uid = user['user']['uid']
    pid = user['user']['id']

    access_token = user['token']

    driver.close()
    if len(access_token) > 0:
        return {"error": False, "token": access_token, "message": "SUCCESS", "suid": uid, 'puid': pid}
    else:
        return {"error": True, "message": "UNKNOWN_ERROR"}


@app.route('/login', methods=['POST'])
def browser():
    nid = random.randint(1000000, 9999999)
    logger.info(f'[{nid}] New request')

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        user_profile = request.json
    else:
        user_profile = {username: request.args.get(
            "username"), password: request.args.get("password")}
        

    try:
        return_data = perfomance_login(user_profile, nid)
    except Exception as e:
        logger.info(e)
        return {"error": True, "message": "UNKNOWN_ERROR"}
    return return_data
    
    


if __name__ == '__main__':

    # logger.info('Testing')
    # options = uc.ChromeOptions()

    # prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    # options.add_experimental_option("prefs", prefs)
    # options.add_argument('-no-first-run')
    # options.add_argument('-force-color-profile=srgb')
    # options.add_argument('-metrics-recording-only')
    # options.add_argument('-password-store=basic')
    # options.add_argument('-use-mock-keychain')
    # options.add_argument('-export-tagged-pdf')
    # options.add_argument('-no-default-browser-check')
    # options.add_argument('-disable-background-mode')
    # options.add_argument('-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions')
    # options.add_argument('-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage')
    # options.add_argument('-deny-permission-prompts')
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--clear-data")
    
    # options.add_argument("--incognito")
    # options.add_argument("--disable-blink-features=AutomationControlled")


    # driver = uc.Chrome(options=options,headless=True)
    # driver.get("https://www.google.com.vn/")
    # js = '''
    #     let callback = arguments[0];
    #     let xhr = new XMLHttpRequest();
    #     xhr.open('GET', 'https://www.google.com.vn/', true);
    #     xhr.onload = function () {
    #         if (this.readyState === 4) {
    #             callback(this.status);
    #         }
    #     };
    #     xhr.onerror = function (err) {
    #         console.log(err);
    #         callback('error');
    #     };
    #     xhr.send(null);
    # '''
    
    # status_code = driver.execute_async_script(js)
    
    # if status_code in [200, 301, 302]:
    #     logger.info("Seleium OK")
    # else:
    #     raise Exception("Selenium failed")
    # driver.close()
    app.run(threaded=False, processes=8, host="0.0.0.0", port=os.getenv("PORT"))






