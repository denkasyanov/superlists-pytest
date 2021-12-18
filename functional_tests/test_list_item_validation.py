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

    # The home page refreshes, and there is an error message saying
    # that list items cannot be blank

    wait_for(
        lambda: assertHTMLEqual(
            browser.find_element(By.CSS_SELECTOR, ".has-errors").text,
            "You can't have an empty list item",
        )
    )
    ### element = WebDriverWait(browser, 3).until(
    ###     EC.presence_of_element_located((By.CSS_SELECTOR, ".has-error"))
    ### )
    ### assert element.text == "You can't have an empty list item"

    # She tries again with some text for the item, which now works
    get_item_input_box(browser).send_keys("Buy milk")
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Perversely, she now decides to submit a second blank list item
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    wait_for(
        lambda: assertHTMLEqual(
            browser.find_element(By.CSS_SELECTOR, ".has-errors").text,
            "You can't have an empty list item",
        )
    )

    # And she can correct it by filling some text in
    get_item_input_box(browser).send_keys("Make tea")
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for_row_in_list_table(browser, "2: Make tea")
