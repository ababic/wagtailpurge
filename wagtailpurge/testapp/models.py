from django.db import models

from wagtail.images.models import AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    file_hash = models.CharField(
        blank=True, db_index=True, editable=False, max_length=40
    )


class Rendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, related_name="renditions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
