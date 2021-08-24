from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .constants import RequestStatusChoices


class RelevantStatusFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("status")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "status"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        values_of_interest = set(
            model_admin.get_queryset(request)
            .values_list("status", flat=True)
            .distinct()
        )
        # always include these statuses
        values_of_interest.update(
            [RequestStatusChoices.NEW, RequestStatusChoices.COMPLETED]
        )
        return tuple(
            ch for ch in RequestStatusChoices.choices if ch[0] in values_of_interest
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()
        if value is not None:
            return queryset.filter(status=value)
        return queryset
