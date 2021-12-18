from selenium.webdriver.common.by import By


def get_item_input_box(browser):
    return browser.find_element(By.ID, "id_text")
