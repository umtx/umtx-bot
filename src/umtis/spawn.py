import json
import time
import seleniumwire.undetected_chromedriver.v2 as uc

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent import futures
import random

from umtis.fetch import main as fetch_main
from umtis.seleniumpro.local_storage import LocalStorage
from umtis import log

logger = log.setup_logging("SIS")


def fill_button_xpath(driver: webdriver, xpath_value: str, value: str):
    sleep_and_wait(1)
    while len(driver.find_elements(By.XPATH, xpath_value)) < 1:
        logger.warn('Wait')

        sleep_and_wait(2)
    if ((not driver.find_elements(By.XPATH, xpath_value)[0].is_displayed()) or (not driver.find_elements(By.XPATH, xpath_value)[0].is_enabled())):
        sleep_and_wait(3)
    else:
        sleep_and_wait(1)
        driver.find_elements(By.XPATH, xpath_value)[0].send_keys(value)



def click_button_xpath(driver: webdriver, xpath_value: str):
    sleep_and_wait(1)

    while len(driver.find_elements(By.XPATH, xpath_value)) < 1:
        logger.warn('Wait')
        sleep_and_wait(2)
    # sl
    if ((not driver.find_elements(By.XPATH, xpath_value)[0].is_displayed()) or (not driver.find_elements(By.XPATH, xpath_value)[0].is_enabled())):
        sleep_and_wait(3)
    else:
        sleep_and_wait(1)

        driver.find_elements(By.XPATH, xpath_value)[0].click()


def sleep_and_wait(seconds: int):
    time.sleep(seconds)


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return result_str


def browser(thread):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--headless")

    driver = uc.Chrome(options=chrome_options, seleniumwire_options={
        'mitm_websocket': False,

        'verify_ssl': False,
        'ssl_cert_verify': False
    })

    #
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source":
    #         "const newProto = navigator.__proto__;"
    #         "delete newProto.webdriver;"
    #         "navigator.__proto__ = newProto;"
    # })
    #
    logger.info("Go to https://sis.umt.edu.vn/")
    driver.get('https://sis.umt.edu.vn/')
    # sleep_and_wait(2)
    click_button_xpath(driver, "//span[@class='menu-icon d-block']")

    fill_button_xpath(driver, "//input[@id='i0116']", "binh.2201700002@st.umt.edu.vn")
    # username_section = driver.find_elements(By.XPATH, "//input[@id='i0116']")
    # username_section[0].send_keys()
    click_button_xpath(driver, '//input[@id="idSIButton9"]')
    logger.info("Input email")

    fill_button_xpath(driver, '//input[@id="i0118"]', "@Altwis2707@")

    logger.info("Input password")

    click_button_xpath(driver, '//input[@id="idSIButton9"]')

    click_button_xpath(driver, '//input[@id="idSIButton9"]')

    logger.info("Login")

    sleep_and_wait(3)
    # print(driver)
    for request in driver.requests:
        if str(request.url).find("https://apisis.umt.edu.vn/api/v1.0/select/academicyears") > -1:
            if "authorization" in request.headers:
                access_token = request.headers["authorization"]

    logger.info("Done fetching TOKEN")

    lcs = LocalStorage(driver)
    user = json.loads(lcs.get("sis-auth-react"))
    uid = user['user']['uid']
    logger.info("TOKEN: " + str(access_token))
    driver.close()
    fetch_main(access_token, uid)


def authorize():
    # instance of Options class allows
    # us to configure Headless Chrome
    threads = 1
    with futures.ThreadPoolExecutor() as executor:
        future_test_results = [executor.submit(browser, i)
                               for i in range(1, int(threads) + 1)]
        for future_test_result in future_test_results:
            test_result = future_test_result.result()
