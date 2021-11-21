import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def test_layout_and_styling(live_server_url, browser, wait_for_row_in_list_table):
    # Edith goes to the home page
    browser.get(live_server_url)
    browser.set_window_size(1024, 768)

    # She notices the input box is nicely centered
    inputbox = browser.find_element(By.ID, "id_new_item")
    assert inputbox.location["x"] + inputbox.size["width"] / 2 == pytest.approx(
        512, abs=10
    )

    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.send_keys("testing")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: testing")
    inputbox = browser.find_element(By.ID, "id_new_item")
    assert inputbox.location["x"] + inputbox.size["width"] / 2 == pytest.approx(
        512, abs=10
    )
