from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import resolve

from pytest_django.asserts import assertTemplateUsed

from lists.views import home_page


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")
