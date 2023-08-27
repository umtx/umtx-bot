from flask import Flask, render_template, request
import json
import time
import seleniumwire.undetected_chromedriver.v2 as uc

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
def spawn():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = uc.Chrome(options=chrome_options, seleniumwire_options={
    'mitm_websocket': False,

    'verify_ssl': False,
    'ssl_cert_verify': False
    })
    time.sleep(1000)
    
if __name__ == "__main__":
    spawn()