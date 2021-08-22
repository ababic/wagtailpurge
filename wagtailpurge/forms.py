from django import forms
from django.conf import settings

from wagtail.admin.forms import WagtailAdminModelForm

CACHE_NAME_CHOICES = tuple(
    (key, f"{key} ({val['BACKEND'].split('.')[-1]})")
    for key, val in settings.CACHES.items()
)


class BaseDjangoCachePurgeRequestFormm(WagtailAdminModelForm):
    cache_name = forms.ChoiceField(
        label="Choose a cache to purge",
        required=True,
        choices=CACHE_NAME_CHOICES,
        widget=forms.RadioSelect,
    )
