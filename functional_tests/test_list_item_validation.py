import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pytest_django.asserts import assertHTMLEqual

from .base import get_item_input_box


def test_cannot_add_empty_list_items(
    live_server_url, browser, wait_for_row_in_list_table, wait_for
):
    # Edith goes to the home page and accidentally tries to submit
    # an empty list item. She hits Enter on the empty input box
    browser.get(live_server_url)
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # The browser intercepts the request, and does not load the
    # list page
    wait_for(lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

    # She starts typing some text for the new item and the error disappears
    get_item_input_box(browser).send_keys("Buy milk")
    wait_for(lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))

    # And she can submit it successfully
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    ### element = WebDriverWait(browser, 3).until(
    ###     EC.presence_of_element_located((By.CSS_SELECTOR, ".has-error"))
    ### )
    ### assert element.text == "You can't have an empty list item"

    # Perversely, she now decides to submit a second blank list item
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # Again, the browser will not comply
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for(lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

    # And she can correct it by filling some text in
    get_item_input_box(browser).send_keys("Make tea")
    wait_for(lambda: browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for_row_in_list_table(browser, "2: Make tea")
