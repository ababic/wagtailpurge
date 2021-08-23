from datetime import timedelta

from wagtailpurge.models import DjangoCachePurgeRequest

INDEX_URL = "/admin/wagtailpurge/djangocachepurgerequest/"
SUBMIT_URL = "/admin/wagtailpurge/djangocachepurgerequest/create/"


def test_index_view(admin_client, admin_user):

    # Add a few objects to fully test listing
    DjangoCachePurgeRequest.objects.bulk_create(
        [
            DjangoCachePurgeRequest(
                cache_name="default",
                submitter=admin_user,
                duration=timedelta(microseconds=1),
            ),
            DjangoCachePurgeRequest(
                cache_name="secondary",
                submitter=admin_user,
                duration=timedelta(seconds=1),
            ),
            DjangoCachePurgeRequest(
                cache_name="tertiary",
                submitter=admin_user,
                duration=timedelta(microseconds=500),
            ),
        ]
    )

    # All items should be shown when no filters are applied
    response = admin_client.get(INDEX_URL)
    assert response.status_code == 200
    assert len(response.context["object_list"]) == 3

    # Only matching items should be shown filters are applied
    response = admin_client.get(INDEX_URL, data={"cache_name": "secondary"})
    assert response.status_code == 200
    assert len(response.context["object_list"]) == 1


def test_submit_view_get(admin_client, admin_user):
    response = admin_client.get(SUBMIT_URL)
    assert response.status_code == 200
    assert response.context["form"].instance.submitter == admin_user


def test_submit_view_post(admin_client, admin_user):
    # Avoiding 'default' because clearing an in-user cache is undesirable
    cache_name = "secondary"
    response = admin_client.post(SUBMIT_URL, data={"cache_name": cache_name})

    # Confirm redirected back to index URL
    assert response.status_code == 302
    assert response["Location"] == INDEX_URL

    # Confirm object creation
    assert DjangoCachePurgeRequest.objects.all().exists()
    obj = DjangoCachePurgeRequest.objects.get()
    assert obj.submitter == admin_user
    assert obj.cache_name == cache_name
    assert obj.submitter_username == admin_user.get_username()


def test_edit_view(admin_client, admin_user):
    obj = DjangoCachePurgeRequest.objects.create(
        cache_name="default", submitter=admin_user
    )
    edit_url = f"{INDEX_URL}edit/{obj.pk}/"

    # Confirm GET requets redirect back to index URL
    response = admin_client.get(edit_url)
    assert response.status_code == 301
    assert response["Location"] == INDEX_URL

    # Confirm POST requets redirect back to index URL
    response = admin_client.post(edit_url)
    assert response.status_code == 301
    assert response["Location"] == INDEX_URL
