from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import resolve

import pytest
from pytest_django.asserts import assertTemplateUsed

from lists.models import Item
from lists.views import home_page

pytestmark = pytest.mark.django_db

# view tests


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_can_save_a_post_request(client):
    response = client.post("/", data={"item_text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_redirects_after_post(client):
    response = client.post("/", data={"item_text": "A new list item"})
    assert response.status_code == 302
    assert response["location"] == "/"


def test_only_saves_items_when_necessary(client):
    client.get("/")
    assert 0 == Item.objects.count()


def test_displays_all_list_items(client):
    Item.objects.create(text="itemey 1")
    Item.objects.create(text="itemey 2")

    response = client.get("/")

    assert "itemey 1" in response.content.decode()
    assert "itemey 2" in response.content.decode()


# model tests


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
