from wagtail.contrib.frontend_cache.backends import BaseBackend


class DummyFECacheBackend(BaseBackend):
    def purge(self, url):
        pass
