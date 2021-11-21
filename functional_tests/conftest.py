import os
import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def live_server_url(live_server):
    staging_server = os.environ.get("STAGING_SERVER")
    if staging_server:
        live_server_url = "http://" + staging_server
    else:
        live_server_url = live_server.url

    yield live_server_url


MAX_WAIT = 5


@pytest.fixture
def wait_for_row_in_list_table():
    def wrapped(browser, row_text):
        start_time = time.time()
        while True:
            try:
                table = browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                assert row_text in [row.text for row in rows]
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return wrapped


@pytest.fixture
def wait_for():
    def wrapped(func):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    return wrapped
