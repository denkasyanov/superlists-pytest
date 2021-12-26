import pytest

from django.contrib.auth import get_user_model

from accounts.models import Token

pytestmark = pytest.mark.django_db


User = get_user_model()


# test user model


def test_user_is_valid_with_email_only():
    user = User(email="a@b.com")
    user.full_clean()


def test_email_is_primary_key():
    user = User(email="a@b.com")
    assert user.pk == "a@b.com"


# test token model


def test_links_user_with_auto_generated_uid():
    token1 = Token.objects.create(email="a@b.com")
    token2 = Token.objects.create(email="a@b.com")
    assert not token1.uid == token2.uid
