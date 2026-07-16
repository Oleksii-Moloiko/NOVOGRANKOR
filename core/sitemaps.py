from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0
    protocol = "https"
    def items(self):
        return [
            "home",
        ]
    
    def location(self, item):
        return reverse(item)