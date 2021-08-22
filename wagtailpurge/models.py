import logging
from typing import Iterable, Sequence

from django.apps import apps
from django.conf import settings
from django.core.cache import caches
from django.db import models
from django.forms.widgets import RadioSelect
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.core.models import Page
from wagtail.core.query import PageQuerySet
from wagtail.images import get_image_model, get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import AbstractRendition

from .constants import APP_ICON, MagnitudeChoices, RequestStatusChoices
from .forms import BaseDjangoCachePurgeRequestFormm

logger = logging.getLogger("purge")


REQUEST_CLASSES = []
FRONTENDCACHE_USED = apps.is_installed("wagtail.contrib.frontend_cache")


class PurgeRequestMetaclass(models.base.ModelBase):
    """Metaclass for BasePurgeRequest"""

    def __init__(cls, name, bases, dct):
        super(PurgeRequestMetaclass, cls).__init__(name, bases, dct)
        if not hasattr(cls, "purge_menu_label"):
            cls.purge_menu_label = str(cls._meta.verbose_name).replace(
                " purge request", ""
            )
        if not hasattr(cls, "purge_menu_icon"):
            cls.purge_menu_icon = APP_ICON
        if not cls._meta.abstract:
            # register this type
            REQUEST_CLASSES.append(cls)


class BasePurgeRequest(ClusterableModel, metaclass=PurgeRequestMetaclass):
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    submitter_username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    error_message = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(
        choices=RequestStatusChoices.choices,
        default=RequestStatusChoices.NEW,
        editable=False,
    )
    status_updated = models.DateTimeField(null=True, editable=False)
    duration = models.DurationField(null=True, editable=False)

    list_display_extra = ()
    list_filter_extra = ()

    class Meta:
        abstract = True

    @classmethod
    def is_enabled(cls) -> bool:
        return True

    def save(self, *args, **kwargs):
        if not self.submitter_username and self.submitter:
            # This change may or may not be saved,
            # depending on the value update_kwargs
            self.submitter_username = self.submitter.get_username()
        super().save(*args, **kwargs)

    def _process(self) -> None:
        self.mark_processing()
        # Used to calculate 'duration' in update_status()
        self._processing_started = timezone.now()
        try:
            self.process()
        except Exception as e:
            self.mark_failed(e)
        else:
            self.mark_complete()

    def process(self) -> None:
        """
        Override this method to apply the correct purge behavior
        for each subclass. Status updates and error logging are
        handled by self._process(), so this method should focus
        on purging only.
        """
        raise NotImplementedError

    def update_status(
        self, status: int, *extra_update_fields: str, set_duration: bool = False
    ) -> None:
        self.status = status
        self.status_updated = timezone.now()

        update_fields = {"status", "status_updated", "error_message", "duration"}

        if set_duration:
            try:
                # self._processing_started is set by ._process()
                self.duration = timezone.now() - self._processing_started
            except (AttributeError, TypeError):
                self.duration = None
            update_fields.add("duration")

        update_fields.update(extra_update_fields)
        self.save(update_fields=update_fields)

    def mark_processing(self) -> None:
        logger.debug(f"Processing: {self}")
        self.update_status(RequestStatusChoices.PROCESSING)

    def mark_failed(self, error: Exception = None) -> None:
        logger.error(f"Error while processing: {self}", exc_info=error)
        self.error_message = str(error)
        self.update_status(RequestStatusChoices.FAILED, set_duration=True)

    def mark_complete(self) -> None:
        logger.debug(f"{self} was processed successfully")
        self.update_status(RequestStatusChoices.COMPLETED, set_duration=True)

    def username(self) -> str:
        if self.submitter:
            return self.submitter.get_username()
        return self.submitter_username

    username.short_description = _("submitted by")

    def execution_time(self) -> str:
        if self.duration:
            seconds = self.duration.total_seconds()
            if seconds < 0.01:
                microseconds = seconds * 1000
                return f"{microseconds:.2f}ms"
            return f"{seconds:.2f}s"
        return "-"

    execution_time.short_description = _("exe. time")
    execution_time.admin_order_field = "duration"


class DjangoCachePurgeRequest(BasePurgeRequest):
    purge_menu_label = _("Django cache")
    base_form_class = BaseDjangoCachePurgeRequestFormm

    cache_name = models.CharField(max_length=255, db_index=True)

    list_display_extra = ["cache_name"]
    list_filter_extra = ["cache_name"]

    class Meta:
        verbose_name = _("Django cache purge request")

    panels = [FieldPanel("cache_name")]

    @classmethod
    def is_enabled(cls) -> bool:
        return bool(settings.CACHES)

    def process(self) -> None:
        """
        Clear the selected Django cache.
        """
        caches[self.cache_name].clear()


class PageURLPurgeRequest(BasePurgeRequest):
    purge_menu_label = _("Page URLs")
    purge_menu_icon = "doc-full-inverse"

    page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Choose a page"),
        null=True,
        on_delete=models.SET_NULL,
    )
    magnitude = models.IntegerField(
        verbose_name=_("purge URLs for"),
        choices=MagnitudeChoices.choices,
        default=MagnitudeChoices.SINGLE,
        db_index=True,
    )
    page_url = models.CharField(verbose_name="page URL", editable=False, max_length=255)
    url_count = models.IntegerField(
        verbose_name=_("URLs purged"), editable=False, null=True
    )

    list_display_extra = ["page_url", "url_count"]

    class Meta:
        verbose_name = _("page URL purge request")

    panels = [PageChooserPanel("page"), FieldPanel("magnitude", widget=RadioSelect())]

    @classmethod
    def is_enabled(cls) -> bool:
        return FRONTENDCACHE_USED

    def get_target_pages(self) -> PageQuerySet:
        queryset = Page.objects.page(self.page)
        if self.magnitude == MagnitudeChoices.CHILDREN:
            queryset |= self.page.get_children()
        elif self.magnitude == MagnitudeChoices.DESCENDANTS:
            queryset |= self.page.get_descendants()
        return queryset

    def process(self) -> None:
        """
        Use PurgeBatch to purge the URLs of all relevant pages.
        """
        purge_batch = PurgeBatch()
        for page in self.get_target_pages().specific(defer=True).iterator():
            purge_batch.add_page(page)

        self.page_url = purge_batch.urls[0]
        self.url_count = len(purge_batch.urls)
        self.save(update_fields=["page_url", "url_count"])
        purge_batch.purge()


class ImageRenditionsPurgeRequest(BasePurgeRequest):
    purge_menu_label = _("Image renditions")
    purge_menu_icon = "image"

    image_count = models.IntegerField("images selected", editable=False, null=True)
    rendition_count = models.IntegerField(
        verbose_name=_("renditions purged"), editable=False, null=True
    )

    class Meta:
        verbose_name = _("image rendition purge request")

    panels = [InlinePanel("images", min_num=1)]

    list_display_extra = ["image_count", "rendition_count"]

    @classmethod
    def is_enabled(cls) -> bool:
        return "wagtail.images" in settings.INSTALLED_APPS

    @cached_property
    def target_image_ids(self) -> Sequence[int]:
        return tuple(
            self.images.all().values_list("image_id", flat=True).distinct("image_id")
        )

    def get_target_renditions(self) -> Iterable[AbstractRendition]:
        model = get_image_model().get_rendition_model()
        return model.objects.filter(image_id__in=self.target_image_ids)

    def process(self) -> None:
        """
        Delete renditions for the selected image, storing the
        number of affected renditions in the 'total' field.

        If the 'wagtail.contrib.PageURL' app is installed,
        purge requests will also be triggered for rendition URLs.
        """
        self.image_count = len(self.target_image_ids)
        renditions = self.get_target_renditions()
        self.purge_rendition_urls(renditions)
        self.image_count = len(self.target_image_ids)
        self.rendition_count = len(renditions)
        renditions.delete()
        self.save(update_fields=["image_count", "rendition_count"])

    @staticmethod
    def purge_rendition_urls(renditions: Iterable[AbstractRendition]) -> None:
        if not FRONTENDCACHE_USED:
            return

        purge_batch = PurgeBatch()
        for r in renditions:
            purge_batch.add_url(r.url)
        purge_batch.purge()


class RenditionsPurgeRequestImage(models.Model):
    purge_request = ParentalKey(
        ImageRenditionsPurgeRequest, related_name="images", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        get_image_model_string(),
        verbose_name=_("image"),
        on_delete=models.SET_NULL,
        null=True,
    )
    panels = [ImageChooserPanel("image")]
