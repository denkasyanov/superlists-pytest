from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import resolve
from django.utils.html import escape

import pytest
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)
from lists.forms import EMPTY_ITEM_ERROR, ItemForm

from lists.models import Item, List
from lists.views import home_page

pytestmark = pytest.mark.django_db

# view tests


def test_home_page_returns_correct_html(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


# list view tests


def test_uses_list_template(client):
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")
    assertTemplateUsed(response, "list.html")


def test_passes_correct_list_to_template(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = client.get(f"/lists/{correct_list.id}/")
    assert response.context["list"], correct_list


def test_displays_only_items_for_that_list(client):

    correct_list = List.objects.create()
    Item.objects.create(text="itemey 1", list=correct_list)
    Item.objects.create(text="itemey 2", list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text="other list item 1", list=other_list)
    Item.objects.create(text="other list item 2", list=other_list)

    response = client.get(f"/lists/{correct_list.id}/")

    assertContains(response, "itemey 1")
    assertContains(response, "itemey 2")

    assertNotContains(response, "other list item 1")
    assertNotContains(response, "other list item 2")


def test_can_save_a_post_request_to_an_existing_list(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )
    assert Item.objects.count() == 1

    new_item = Item.objects.first()
    assert new_item.text == "A new item for an existing list"
    assert new_item.list == correct_list


def test_post_redirects_to_list_view(client):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f"/lists/{correct_list.id}/",
        data={"text": "A new item for an existing list"},
    )

    assertRedirects(response, f"/lists/{correct_list.id}/")


def post_invalid_input(client):
    list_ = List.objects.create()
    return client.post(f"/lists/{list_.id}/", data={"text": ""})


def test_for_invalid_input_nothing_saved_to_db(client):
    post_invalid_input(client)
    assert Item.objects.count() == 0


def test_for_invalid_input_renders_list_template(client):
    response = post_invalid_input(client)
    assert response.status_code == 200
    assertTemplateUsed(response, "list.html")


def test_for_invalid_input_passes_form_to_template(client):
    response = post_invalid_input(client)
    assert isinstance(response.context["form"], ItemForm)


def test_for_invalid_input_shows_error_on_page(client):
    response = post_invalid_input(client)
    assertContains(response, escape(EMPTY_ITEM_ERROR))


@pytest.mark.skip()
def test_duplicate_item_validation_errors_end_up_on_lists_page(client):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="textey")

    response = client.post(f"/lists/{list1.id}/", data={"text": "textey"})

    expected_error = escape("You've already got this in your list")
    assertContains(response, expected_error)
    assertTemplateUsed(response, "list.html")
    assert Item.objects.all().count() == 1


def test_displays_item_form(client):
    list_ = List.objects.create()
    response = client.get(f"/lists/{list_.id}/")
    assert isinstance(response.context["form"], ItemForm)
    assertContains(response, 'name="text"')


# new list tests


def test_can_save_a_post_request(client):
    response = client.post("/lists/new", data={"text": "A new list item"})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == "A new list item"


def test_redirects_after_post(client):
    response = client.post("/lists/new", data={"text": "A new list item"})
    list_ = List.objects.first()
    assertRedirects(response, f"/lists/{list_.id}/")


def test_for_invalid_input_renders_home_template(client):
    response = client.post("/lists/new", data={"text": ""})
    assert response.status_code == 200
    assertTemplateUsed(response, "home.html")


def test_validation_erros_are_shown_on_home_page(client):
    response = client.post("/lists/new", data={"text": ""})
    assertContains(response, escape(EMPTY_ITEM_ERROR))


def test_for_invalid_input_passes_form_to_template(client):
    response = client.post("/lists/new", data={"text": ""})
    assert isinstance(response.context["form"], ItemForm)


def test_invalid_list_items_are_not_saved(client):
    client.post("/lists/new", data={"text": ""})
    assert List.objects.count() == 0
    assert Item.objects.count() == 0


# home page tests


def test_uses_home_template(client):
    response = client.get("/")
    assertTemplateUsed(response, "home.html")


def test_home_page_uses_item_form(client):
    response = client.get("/")
    assert isinstance(response.context["form"], ItemForm)
