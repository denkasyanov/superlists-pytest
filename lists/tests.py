from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import resolve

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item
from lists.views import home_page


# view tests


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_can_save_a_post_request(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert "A new list item" in response.content.decode()
    assertTemplateUsed(response, "home.html")


# model tests


@pytest.mark.django_db
def test_saving_and_retrieveing_items():
    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    assert first_saved_item.text == "The first (ever) list item"

    second_saved_item = saved_items[1]
    assert second_saved_item.text == "Item the second"
