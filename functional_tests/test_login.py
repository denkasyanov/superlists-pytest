import re

import pytest
from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .base import assertIn


TEST_EMAIL = "edith@example.com"
SUBJECT = "Your login link for Superlists"


def test_can_get_email_link_to_log_in(live_server_url, browser, wait_for):
    # Edith goes to the awesome superlists site
    # and notices a "Log in" section in the navbar for the first time
    # It's telling her to enter her email address, so she does
    browser.get(live_server_url)
    browser.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    browser.find_element(By.NAME, "email").send_keys(Keys.ENTER)

    # A message appears telling her an email has been sent
    wait_for(
        lambda: assertIn(
            "Check your email", browser.find_element(By.TAG_NAME, "body").text
        )
    )

    # She checks her email and finds a message
    email = mail.outbox[0]
    assert TEST_EMAIL in email.to
    assert email.subject == SUBJECT

    # It has a url link in it
    assert "Use this link to log in" in email.body
    url_search = re.search(r"http://.+/.+$", email.body)
    if not url_search:
        pytest.fail(f"Could not find url in email body:\n{email.body}")
    url = url_search.group(0)
    assert live_server_url in url

    # she clicks it
    browser.get(url)

    # she is logged in!
    wait_for(lambda: browser.find_element(By.LINK_TEXT, "Log out"))
    navbar = browser.find_element(By.CSS_SELECTOR, ".navbar")
    assert TEST_EMAIL in navbar.text

    # Now she logs out
    browser.find_element(By.LINK_TEXT, "Log out").click()

    # She is logged out
    wait_for(lambda: browser.find_element(By.NAME, "email"))
    navbar = browser.find_element(By.CSS_SELECTOR, ".navbar")
    assert TEST_EMAIL not in navbar.text
