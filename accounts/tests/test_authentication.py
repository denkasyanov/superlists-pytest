import pytest

from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()


pytestmark = pytest.mark.django_db

# authenticate() tests


def test_returns_none_if_no_such_token():
    result = PasswordlessAuthenticationBackend().authenticate(
        "f4f3d595-e305-4527-b957-aa2b1e6fa324"
    )
    assert result is None


def test_returns_new_user_with_correct_email_if_token_exists():
    email = "edith@example.com"
    token = Token.objects.create(email=email)
    authenticated_user = PasswordlessAuthenticationBackend().authenticate(token.uid)
    user_by_email = User.objects.get(email=email)
    assert authenticated_user == user_by_email


def test_returns_existing_user_with_correct_email_if_token_exists():
    email = "edith@example.com"
    existing_user = User.objects.create(email=email)
    token = Token.objects.create(email=email)
    user = PasswordlessAuthenticationBackend().authenticate(token.uid)
    assert user == existing_user


# get_user() tests


def test_gets_user_by_email():
    User.objects.create(email="another@example.com")
    desired_user = User.objects.create(email="edith@example.com")
    found_user = PasswordlessAuthenticationBackend().get_user("edith@example.com")
    assert found_user == desired_user


def test_returns_none_if_no_user_with_that_email():
    assert PasswordlessAuthenticationBackend().get_user("edith@example.com") is None
