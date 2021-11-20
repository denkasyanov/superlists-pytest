from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import resolve

from pytest_django.asserts import assertTemplateUsed

from lists.views import home_page


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_can_save_a_post_request(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert "A new list item" in response.content.decode()
    assertTemplateUsed(response, "home.html")
