import re
import time

import pytest
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


def check_for_row_in_list_table(browser, row_text):
    table = browser.find_element(By.ID, "id_list_table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    assert row_text in [row.text for row in rows]


MAX_WAIT = 5


def wait_for_row_in_list_table(browser, row_text):
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


# new visitor


def test_can_start_a_list_for_one_user(live_server, browser):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)

    # She notices the page title and header mention to-do lists
    assert "To-Do" in browser.title
    header_text = browser.find_element(By.TAG_NAME, "h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away
    inputbox = browser.find_element(By.ID, "id_new_item")
    assert inputbox.get_attribute("placeholder") == "Enter a to-do item"

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    inputbox.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    inputbox = browser.find_element(By.ID, "id_new_item")
    inputbox.send_keys("Use peacock feathers to make a fly")
    inputbox.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    wait_for_row_in_list_table(browser, "2: Use peacock feathers to make a fly")
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # Satisfied, she goes back to sleep


def test_multiple_users_can_start_lists_at_different_urls(live_server, browser):
    # Edith starts a new to-do list
    browser.get(live_server.url)
    inputbox = browser.find_element(By.ID, "id_new_item")
    inputbox.send_keys("Buy peacock feathers")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy peacock feathers")

    # She notices that her list has a unique URL
    edith_list_url = browser.current_url
    assert re.search("/lists/.+", edith_list_url)

    # Now a new user, Francis, comes along to the site.
    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies etc
    browser.quit()

    browser = webdriver.Firefox()
    # Francis visits the home page.  There is no sign of Edith's
    # list
    browser.get(live_server.url)
    page_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Buy peacock feathers" not in page_text
    assert "make a fly" not in page_text

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
    inputbox = browser.find_element(By.ID, "id_new_item")
    inputbox.send_keys("Buy milk")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Francis gets his own unique URL
    francis_list_url = browser.current_url
    assert re.search("/lists/.+", francis_list_url)
    assert edith_list_url != francis_list_url

    page_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Buy peacock feathers" not in page_text
    assert "Buy milk" in page_text

    browser.quit()
