from unittest.mock import patch

import pytest
from pytest_django.asserts import assertRedirects

from accounts.models import Token


pytestmark = pytest.mark.django_db

# send login email view tests


def test_redirects_to_home_page(client):
    response = client.post(
        "/accounts/send_login_email/", data={"email": "edith@example.com"}
    )
    assertRedirects(response, "/")


mail_details = {
    "send_mail_called": False,
}


def fake_send_mail(subject, body, from_email, to_list):
    global mail_details
    mail_details.update(
        {
            "send_mail_called": True,
            "subject": subject,
            "body": body,
            "from_email": from_email,
            "to_list": to_list,
        }
    )


@patch("accounts.views.send_mail")
def test_sends_email_to_address_from_post(mock_send_mail, client):
    client.post("/accounts/send_login_email/", data={"email": "edith@example.com"})

    assert mock_send_mail.called
    (subject, body, from_email, to_list), _ = mock_send_mail.call_args

    assert subject == "Your login link for Superlists"
    assert from_email == "noreply@superlists"
    assert to_list == ["edith@example.com"]


def test_adds_success_message(client):
    response = client.post(
        "/accounts/send_login_email/", data={"email": "edith@example.com"}, follow=True
    )

    message = list(response.context["messages"])[0]
    assert (
        message.message
        == "Check your email, we've sent you a link you can use to log in."
    )
    assert message.tags == "success"


def test_creates_token_associated_with_email(client):
    client.post("/accounts/send_login_email/", data={"email": "edith@example.com"})

    token = Token.objects.first()
    assert token.email == "edith@example.com"


@patch("accounts.views.send_mail")
def test_sends_link_to_login_using_token_uid(mock_send_mail, client):
    client.post("/accounts/send_login_email/", data={"email": "edith@example.com"})

    token = Token.objects.first()
    expected_url = f"http://testserver/accounts/login/?token={token.uid}"
    (subject, body, from_email, to_list), _ = mock_send_mail.call_args
    assert expected_url in body


# login view tests


def test_redirects_to_home_page(client):
    response = client.get("/accounts/login/?token=abcd123")
    assertRedirects(response, "/")
