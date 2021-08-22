from typing import Iterable, Sequence, Type

from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup

from .constants import APP_ICON
from .models import REQUEST_CLASSES
from .views import PurgeRequestSubmitView


class PurgeRequestButtonHelper(ButtonHelper):
    def add_button(self, classnames_add=None, classnames_exclude=None):
        values = super().add_button(classnames_add, classnames_exclude)
        values.update(
            label=_("Submit"),
            title=_("Submit a new %s") % self.verbose_name,
        )
        return values


class PurgeRequestModelAdmin(ModelAdmin):
    button_helper_class = PurgeRequestButtonHelper
    create_view_class = PurgeRequestSubmitView
    create_template_name = "modeladmin/wagtailpurge/create.html"
    list_display = ["username", "created_at", "status", "error_message", "exec_time"]
    list_filter = ["status", "created_at"]
    list_select_related = True
    ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_icon = self.model.purge_menu_icon

    def get_menu_label(self):
        return self.model.purge_menu_label

    def username(self, obj):
        if obj.submitter:
            return obj.submitter.get_username()
        return obj.submitter_username

    username.short_description = _("submitter")

    def exec_time(self, obj):
        if obj.duration:
            seconds = obj.duration.total_seconds()
            if seconds < 0.01:
                microseconds = seconds * 1000
                return f"{microseconds:.2f}ms"
            return f"{seconds:.2f}s"

    exec_time.short_description = _("exec. time")
    exec_time.admin_order_field = "duration"


class WagtailPurgeModelAdmin(ModelAdminGroup):
    menu_icon = APP_ICON
    menu_label = "Purge"

    @classproperty
    def items(cls) -> Sequence[Type]:
        return list(cls.generate_children())

    @classmethod
    def generate_children(cls) -> Iterable[Type]:
        for model in [rq for rq in REQUEST_CLASSES if rq.is_enabled()]:
            attrs = {
                "model": model,
                "list_display": list(model.list_display_extra or ())
                + PurgeRequestModelAdmin.list_display,
                "list_filter": list(model.list_filter_extra or ())
                + PurgeRequestModelAdmin.list_filter,
            }
            yield type(
                str(model.__name__ + "ModelAdmin"), (PurgeRequestModelAdmin,), attrs
            )
