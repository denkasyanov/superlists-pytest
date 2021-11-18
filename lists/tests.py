from django.urls import resolve
from lists.views import home_page


def test_root_url_resolvers_to_home_page_view():
    found = resolve("/")
    assert found.func == home_page
