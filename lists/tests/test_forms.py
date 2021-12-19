import pytest

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


def test_form_item_input_has_placeholder_and_css_classes():
    form = ItemForm()
    assert 'placeholder="Enter a to-do item"' in form.as_p()
    assert 'class="form-control input-lg' in form.as_p()


def test_form_validation_for_blank_items():
    form = ItemForm(data={"text": ""})
    assert not form.is_valid()
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]


@pytest.mark.django_db
def test_form_save_handles_saving_to_a_list():
    list_ = List.objects.create()
    form = ItemForm(data={"text": "do me"})
    new_item = form.save(for_list=list_)

    assert new_item == Item.objects.first()
    assert new_item.text == "do me"
    assert new_item.list == list_
