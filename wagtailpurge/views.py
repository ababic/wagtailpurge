import asyncio

from asgiref.sync import sync_to_async
from django.utils.functional import cached_property

from wagtail.contrib.modeladmin.views import CreateView


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
