from wagtail.contrib.modeladmin.options import modeladmin_register

from .modeladmin import WagtailPurgeModelAdmin

modeladmin_register(WagtailPurgeModelAdmin)
