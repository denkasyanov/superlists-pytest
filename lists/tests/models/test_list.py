import pytest

from lists.models import List


pytestmark = pytest.mark.django_db


def test_get_absolute_url():
    list_ = List.objects.create()
    assert list_.get_absolute_url() == f"/lists/{list_.id}/"
