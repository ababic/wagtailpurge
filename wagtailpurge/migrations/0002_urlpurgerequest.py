# Generated by Django 3.2.6 on 2021-11-11 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailpurge", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="URLPurgeRequest",
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
                    "url",
                    models.URLField(
                        help_text="Please enter a full URL, including the scheme and domain (e.g. https://www.example.com/some-url).",
                        max_length=255,
                        verbose_name="URL",
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
                "abstract": False,
            },
        ),
    ]