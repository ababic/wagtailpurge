from unittest import mock

from django.core.cache import caches

from wagtail.contrib.frontend_cache.utils import PurgeBatch

from wagtailpurge.models import (
    DjangoCachePurgeRequest,
    ImageRenditionsPurgeRequest,
    PageURLPurgeRequest,
    URLPurgeRequest,
)


def test_djangocachepurgerequest_process(admin_user):
    # Avoiding 'default' because clearing an in-use cache is undesirable
    cache_name = "secondary"
    cache = caches[cache_name]

    # Create a purge request
    obj = DjangoCachePurgeRequest.objects.create(
        cache_name="secondary",
        submitter=admin_user,
    )

    # Check that processing the request clears the specified cache
    with mock.patch.object(cache, "clear") as mocked_clear:
        obj.process()
        mocked_clear.assert_called_once()


def test_urlpurgerequest_process(admin_user):

    url = "https://www.example.com/some-url"

    # Create a purge request
    obj = URLPurgeRequest.objects.create(url=url, submitter=admin_user)

    # Process the request with a mock PurgeBatch instance
    mock_purge_batch = mock.Mock(spec_set=PurgeBatch)
    with mock.patch.object(
        URLPurgeRequest, "get_purge_batch", return_value=mock_purge_batch
    ):
        obj.process()

    # Check that process() interacted with the PurgeBatch instance as expected
    mock_purge_batch.add_url.assert_called_once_with(url)
    mock_purge_batch.purge.assert_called_once()


def test_pageurlpurgerequest_process(admin_user):
    pass


def test_imagerenditionspurgerequest_process(admin_user):
    pass
