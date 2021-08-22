# wagtailpurge

Trigger cache purges from within the Wagtail CMS. The app is tested for compatibility with:
- Django >= 3.1
- Wagtail >= 2.12

## Get started

1. Install this app with `pip install wagtailpurge`
2. Add `wagtailpurge` to your `INSTALLED_APPS`
3. Log into Wagtail and look out for the **Purge** menu item :)

By default, only **superusers** can submit purge requests, but permissions for individual request types can easily be applied to your existing groups to make the functionality available to others.

## What can I purge?

### Django caches

Utilizes Django's low-level cache API to clear a cache from your project's `CACHES` setting value.

NOTE: This option is only available when `CACHES` contains at least one item.

### Wagtail page URLs

Utilizes Wagtail's `wagtail.contrib.frontend_cache` app to purge selected page URLs from a CDN or upstream cache. You can easily purge sections of the tree by choosing to purge children or descendants of the selected page.

NOTE: This option is only available when `wagtail.contrib.frontend_cache` is installed.

### Wagtail image renditions

Deletes all existing renditions for a Wagtail image (or images) of your choosing. If the `wagtail.contrib.frontend_cache` app is installed, purge requests will also be sent to your CDN or upstream cache for the URL of each rendition, allowing the users to download freshly generated ones. 

### Custom purge requests

If you want to purge something different, it's possible to add your own purge request type. The process is easier than you might think, as everything is defined on the model class. The only requirements are that you use the included `BasePurgeRequest` class as a base, and that you add a `process()` method to handle the actual 'purging' for each request. Here's an example:

```
from django.db import models
from django.forms.widgets import RadioSelect
from wagtailcache.models import BasePurgeRequest
from .utils import purge_naughty_monkey


class NaughtinessCategoryChoices(models.TextChoices):
    BITING = "biting", "Biting"
    SCRATCHING = "scratching", "Scratching"
    TOMFOOLERY = "tomfoolery", "General tomfoolery"


class NaughtyMonkeyPurgeRequest(BasePurgeRequest):
    # Add custom fields
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30,
        choices=NaughtinessCategoryChoices.choices
    )

    # Add panels to show custom fields in the submit form
    panels = (
        FieldPanel("name"),
        FieldPanel("category", widget=RadioSelect())
    )

    # Optionally override the menu label and icon
    purge_menu_label = "Naughty monkey"
    purge_menu_icon = "warning"

    # Optionally add columns to the listing
    list_display_extra = ["name", "category", "custom_method"]

    # Optionally add filter options to the listing
    list_filter_extra = ["category"]

    def process(self) -> None:
        """
        Implemenst 'handling' for this request. The method doesn't need to
        return anything, and any exceptions raised here will be logged
        automatically.
        """
        purge_naughty_monkey(self.name, self.category)

    def custom_method(self) -> str:
        """
        Include non-field columns in the listing by adding a model
        method to return what you need, and include the method name
        in `list_display_extra`.
        """
        return "Custom value"
```
