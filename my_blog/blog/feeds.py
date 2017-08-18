from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

# a model has to have  attribute 'get_absolute_url otherwise cannot incorporate in sitemaps
#otherwise use the following
# item_link is only needed if NewsItem has no get_absolute_url method.
'''def item_link(self, item):
    return reverse('news-item', args=[item.pk])'''
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return truncatewords(item.body, 30)
