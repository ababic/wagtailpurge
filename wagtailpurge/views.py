import asyncio

from asgiref.sync import sync_to_async
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.contrib.modeladmin.views import CreateView, EditView


async def process_purge_request(obj):
    await sync_to_async(obj._process, thread_sensitive=False)()


class PurgeRequestSubmitView(CreateView):
    def get_index_url(self):
        return self.model.list_url

    def get_add_url(self):
        return self.model.submit_url

    @cached_property
    def instance(self):
        return self.model(submitter=self.request.user)

    def form_valid(self, form):
        resp = super().form_valid(form)
        asyncio.run(process_purge_request(form.instance))
        return resp


class PurgeRequestEditView(EditView):
    def get(self, request, **kwargs):
        messages.info(
            request, _('Purge requests cannot be edited')
        )
        return redirect(self.index_url, permanent=True)

    def post(self, request, **kwargs):
        return self.get(request, **kwargs)
