from django.contrib.sitemaps import Sitemap
from .models import Post

# a model has to have  attribute 'get_absolute_url otherwise cannot incorporate in sitemaps
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish
