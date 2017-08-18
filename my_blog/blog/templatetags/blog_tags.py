from django import template
register = template.Library()
from ..models import Post
from django.db.models import Count
from hitcount.models import HitCount
# for actual models always see the code of the app on github

@register.simple_tag
def total_posts(user=None):
    if user==None:
        return Post.published.count()
    else:
        return Post.objects.filter(status='published',author=user).count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    viewed_posts = HitCount.objects.order_by('-hits')[:count]
    return {'latest_posts': latest_posts,'viewed_posts':viewed_posts}


'''@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]'''


'''
#either use this or directrly use safe instead of markdown in template.
#pip install Markdown==2.6.8
from django.utils.safestring import mark_safe
import markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))'''
