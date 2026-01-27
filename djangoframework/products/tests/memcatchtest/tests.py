from django.test import TestCase
from django.core.cache import cache


class CacheConnectionTest(TestCase):

    def test_cache_connection(self):
        cache.set("test", "testing",60)
        self.assertEqual(cache.get("test"), "testing")