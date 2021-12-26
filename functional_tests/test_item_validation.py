from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .base import assertTrue, get_error_element, get_item_input_box


def test_error_messages_are_cleared_out_on_input(
    live_server_url, browser, wait_for, wait_for_row_in_list_table
):
    # Edith starts a list and causes a validation error:
    browser.get(live_server_url)
    get_item_input_box(browser).send_keys("Banter too thick")
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Banter too thick")

    get_item_input_box(browser).send_keys("Banter too thick")
    get_item_input_box(browser).send_keys(Keys.ENTER)

    wait_for(lambda: assertTrue(get_error_element(browser).is_displayed()))

    # She starts typing in the input box to clear the error
    get_item_input_box(browser).send_keys("a")

    # She starts typing in the input box to clear the error
    wait_for(lambda: assertTrue(not get_error_element(browser).is_displayed()))
