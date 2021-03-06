# Generated by Django 3.2.6 on 2021-08-20 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(
            getattr(settings, "WAGTAILIMAGES_IMAGE_MODEL", "wagtailimages.Image")
        ),
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageRenditionsPurgeRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submitter_username", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("error_message", models.TextField(blank=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "New"),
                            (1, "Rejected"),
                            (2, "Approved"),
                            (3, "Processing"),
                            (4, "Cancelled"),
                            (5, "Failed"),
                            (6, "Completed"),
                        ],
                        default=0,
                        editable=False,
                    ),
                ),
                ("status_updated", models.DateTimeField(editable=False, null=True)),
                ("duration", models.DurationField(editable=False, null=True)),
                (
                    "image_count",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="images selected"
                    ),
                ),
                (
                    "rendition_count",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="renditions purged"
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "image rendition purge request",
            },
        ),
        migrations.CreateModel(
            name="RenditionsPurgeRequestImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=getattr(
                            settings, "WAGTAILIMAGES_IMAGE_MODEL", "wagtailimages.Image"
                        ),
                        verbose_name="image",
                    ),
                ),
                (
                    "purge_request",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="wagtailpurge.imagerenditionspurgerequest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PageURLPurgeRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submitter_username", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("error_message", models.TextField(blank=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "New"),
                            (1, "Rejected"),
                            (2, "Approved"),
                            (3, "Processing"),
                            (4, "Cancelled"),
                            (5, "Failed"),
                            (6, "Completed"),
                        ],
                        default=0,
                        editable=False,
                    ),
                ),
                ("status_updated", models.DateTimeField(editable=False, null=True)),
                ("duration", models.DurationField(editable=False, null=True)),
                (
                    "magnitude",
                    models.IntegerField(
                        choices=[
                            (1, "The selected page only"),
                            (2, "The selected page and its direct children"),
                            (3, "The selected page and all of its descendants"),
                        ],
                        db_index=True,
                        default=1,
                        verbose_name="purge URLs for",
                    ),
                ),
                (
                    "page_url",
                    models.CharField(
                        editable=False, max_length=255, verbose_name="page URL"
                    ),
                ),
                (
                    "url_count",
                    models.IntegerField(
                        editable=False, null=True, verbose_name="URLs purged"
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailcore.page",
                        verbose_name="Choose a page",
                    ),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "page URL purge request",
            },
        ),
        migrations.CreateModel(
            name="DjangoCachePurgeRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("submitter_username", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("error_message", models.TextField(blank=True)),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "New"),
                            (1, "Rejected"),
                            (2, "Approved"),
                            (3, "Processing"),
                            (4, "Cancelled"),
                            (5, "Failed"),
                            (6, "Completed"),
                        ],
                        default=0,
                        editable=False,
                    ),
                ),
                ("status_updated", models.DateTimeField(editable=False, null=True)),
                ("duration", models.DurationField(editable=False, null=True)),
                ("cache_name", models.CharField(db_index=True, max_length=255)),
                (
                    "submitter",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Django cache purge request",
            },
        ),
    ]
