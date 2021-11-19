import threading

from asgiref.sync import sync_to_async
from django.db import connection, transaction
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from wagtail.admin import messages
from wagtail.contrib.modeladmin.views import CreateView, EditView


def process_purge_request(obj):
    try:
        obj._process()
    finally:
        # Usually, the request/response cycle will take care of
        # this, but when using threads, we need to make sure
        # DB connections are closed.
        connection.close()


class PurgeRequestSubmitView(CreateView):
    @cached_property
    def instance(self):
        return self.model(submitter=self.request.user)

    def form_valid(self, form):
        resp = super().form_valid(form)
        # once changes are commited to the DB, process the request in a new thread
        thread = threading.Thread(
            target=process_purge_request, args=[form.instance], daemon=True
        )
        transaction.on_commit(thread.start)
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
