import asyncio

from asgiref.sync import sync_to_async
from django.db import transaction
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.contrib.modeladmin.views import CreateView, EditView


async def process_purge_request(obj):
    await sync_to_async(obj._process, thread_sensitive=False)()


class PurgeRequestSubmitView(CreateView):
    @cached_property
    def instance(self):
        return self.model(submitter=self.request.user)

    def form_valid(self, form):
        resp = super().form_valid(form)
        transaction.on_commit(lambda: asyncio.run(process_purge_request(form.instance)))
        return resp

    def get_success_message(self, instance):
        return _("%(model_name)s '%(instance)s' was submitted.") % {
            "model_name": capfirst(self.opts.verbose_name),
            "instance": instance,
        }

    def get_success_message_buttons(self, instance):
        return []


class PurgeRequestEditView(EditView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("Purge requests cannot be edited"))
        return redirect(self.index_url, permanent=True)
