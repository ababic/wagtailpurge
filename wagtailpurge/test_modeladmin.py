from wagtail.admin.menu import admin_menu

import pytest

from wagtailpurge.constants import APP_ICON
from wagtailpurge.models import REQUEST_CLASSES


def test_menu_item_registered():
    purge_menu_item = None
    for item in admin_menu.registered_menu_items:
        if (
            getattr(item, "label", "") == "Purge"
            and getattr(item, "icon_name", "") == APP_ICON
        ):
            purge_menu_item = item
            break
    assert purge_menu_item is not None


@pytest.mark.parametrize("model", [m for m in REQUEST_CLASSES])
def test_index_urls_registered(admin_client, model):
    # Visit the index url for this model
    response = admin_client.get(f"/admin/wagtailpurge/{model.__name__.lower()}/")
    # If the URL weren't registered, this would be a 404
    assert response.status_code == 200


@pytest.mark.parametrize("model", [m for m in REQUEST_CLASSES])
def test_submit_urls_registered(admin_client, model):
    # Visit the submit url for this model
    response = admin_client.get(f"/admin/wagtailpurge/{model.__name__.lower()}/create/")
    # If the URL weren't registered, this would be a 404
    assert response.status_code == 200
