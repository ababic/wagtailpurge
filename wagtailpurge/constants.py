from django.apps import apps
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _

APP_ICON = "fa-bolt" if apps.is_installed("wagtailfontawesome") else "cog"


class MagnitudeChoices(IntegerChoices):
    SINGLE = 1, _("The selected page only")
    CHILDREN = 2, _("The selected page and its direct children")
    DESCENDANTS = 3, _("The selected page and all of its descendants")


class RequestStatusChoices(IntegerChoices):
    NEW = 0, _("New")
    REJECTED = 1, _("Rejected")
    APPROVED = 2, _("Approved")
    PROCESSING = 3, _("Processing")
    CANCELLED = 4, _("Cancelled")
    FAILED = 5, _("Failed")
    COMPLETED = 6, _("Completed")
