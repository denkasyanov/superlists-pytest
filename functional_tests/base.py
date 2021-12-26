from selenium.webdriver.common.by import By


def get_item_input_box(browser):
    return browser.find_element(By.ID, "id_text")


def get_error_element(browser):
    return browser.find_element(By.CSS_SELECTOR, ".has-error")


def assertTrue(test):
    """Hack for using pytest's asserts in the Book's `wait_for` functions."""
    assert test == True


def assertIn(what, where):
    """Hack for using pytest's asserts in the Book's `wait_for` functions."""
    assert what in where
