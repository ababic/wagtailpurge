from typing import Iterable, Sequence, Type

from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.helpers import ButtonHelper, PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup

from .constants import APP_ICON
from .models import REQUEST_CLASSES
from .views import PurgeRequestEditView, PurgeRequestSubmitView


class PurgeRequestPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        # Disables the 'edit' button for all users
        return False


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
    edit_view_class = PurgeRequestEditView
    permission_helper_class = PurgeRequestPermissionHelper
    list_display = [
        "username",
        "created_at",
        "status",
        "error_message",
        "execution_time",
    ]
    list_filter = ["status", "created_at"]
    list_select_related = True
    ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_icon = self.model.purge_menu_icon

    def get_menu_label(self):
        return self.model.purge_menu_label


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
