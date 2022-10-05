# wagtailpurge

Trigger cache purges from within the Wagtail CMS. The app is tested for compatibility with:
- Django >= 3.2
- Wagtail >= 2.16

## Get started

1. Install this app with `pip install wagtailpurge`
2. Add `wagtailpurge` to your `INSTALLED_APPS`
3. From the shell, run `python manage.py migrate wagtailpurge` to create the necessary database tables
4. Log into Wagtail and look out for the **Purge** menu item :)

By default, only **superusers** can submit purge requests, but permissions for individual request types can easily be applied to your existing groups to make the functionality available to others.

## What can I purge?

### 1. Django caches

Utilizes Django's low-level cache API to clear a cache from your project's `CACHES` setting value.

**NOTE:** This option is only available when `CACHES` contains at least one item.

### 2. Individual URLs

Utilizes Wagtail's `wagtail.contrib.frontend_cache` app to purge a single URL of your choosing from a CDN or downstream cache. The URL can be anything from a page URL to a harcoded Django view URL, or even a URL completely out of the app's control (as long as it's on a domain managed by the same CDN / downstream cache account).

**NOTE:** This option is only available when `wagtail.contrib.frontend_cache` is installed.

### 3. Wagtail page URLs

Utilizes Wagtail's `wagtail.contrib.frontend_cache` app to purge selected page URLs from a CDN or downstream cache. You can easily purge sections of the tree by choosing to purge children or descendants of the selected page.

**NOTE:** This option is only available when `wagtail.contrib.frontend_cache` is installed.

### 4. Wagtail image renditions

Deletes all existing renditions for a Wagtail image (or images) of your choosing.

If the `wagtail.contrib.frontend_cache` app is installed, purge requests will also be sent to your CDN or downstream cache for the URL of each rendition, allowing the users to download freshly generated ones.

### 5. Custom purge requests

If you want to purge something else, it's possible to add your own model class with the fields and functionality you need. The only requirements are that you use `BasePurgeRequest` as a base, and that you add a `process()` method to handle the actual 'purging' of each request.

Here is an example:

```
# myproject/purge/models.py

from django.db import models
from django.forms.widgets import RadioSelect
from wagtailcache.models import BasePurgeRequest
from .utils import purge_chimp


class NaughtinessCategoryChoices(models.TextChoices):
    BITING = "biting", "Biting"
    SCRATCHING = "scratching", "Scratching"
    TOMFOOLERY = "tomfoolery", "General tomfoolery"


class NaughtyChimpPurgeRequest(BasePurgeRequest):
    # Add custom fields
    name = models.CharField(
        max_length=100,
        help_text="e.g. Peanuts",
    )
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
    purge_menu_label = "Naughty chimp"
    purge_menu_icon = "warning"

    # Optionally add columns to the listing
    list_display_extra = ["name", "category", "custom_method"]

    # Optionally add filter options to the listing
    list_filter_extra = ["category"]

    def process(self) -> None:
        """
        Implements 'handling' for this purge request. The method doesn't need to
        return anything, and any exceptions raised here will be logged
        automatically.
        """
        purge_chimp(self.name, self.category)

    def custom_method(self) -> str:
        """
        Include non-field columns in the listing by adding a model
        method to return what you need, and including the method name
        in `list_display_extra`.
        """
        return "BANANA!"
```

#### Once you have defined your custom model:

1. Ensure the app with the updated `models.py` (e.g. `"myproject.purge"`) is included in your project's `INSTALLED_APPS` setting.
2. From the shell, run `python manage.py makemigrations appname` to create database migrations for your app.
3. From the shell, run `python manage.py migrate` to apply the migration to your database.
4. Log into Wagtail and look out for your new option in the **Purge** menu :)
