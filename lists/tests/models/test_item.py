from django.core.exceptions import ValidationError
import pytest

from lists.models import Item, List

pytestmark = pytest.mark.django_db


def test_default_text():
    item = Item()
    assert item.text == ""


def test_item_is_related_to_list():
    list_ = List.objects.create()
    item = Item()
    item.list = list_
    item.save()
    assert item in list_.item_set.all()


def test_cannot_save_empty_list_items():
    list_ = List.objects.create()
    item = Item(list=list_, text="")
    with pytest.raises(ValidationError):
        item.save()
        item.full_clean()


def test_duplicate_items_are_invalid():
    list_ = List.objects.create()
    Item.objects.create(list=list_, text="bla")
    with pytest.raises(ValidationError):
        item = Item(list=list_, text="bla")
        item.full_clean()


def test_can_save_item_to_different_lists():
    list1 = List.objects.create()
    list2 = List.objects.create()
    Item.objects.create(list=list1, text="bla")
    item = Item(list=list2, text="bla")
    item.full_clean()


def test_list_ordering():
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text="i1")
    item2 = Item.objects.create(list=list1, text="item 2")
    item3 = Item.objects.create(list=list1, text="i3")
    assert list(Item.objects.all()) == [item1, item2, item3]


def test_string_representation():
    item = Item(text="some text")
    assert str(item) == "some text"
