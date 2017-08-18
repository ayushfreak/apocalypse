from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
url(r'^$', views.post_list, name='post_list'),
url(r'^my_list/(?P<my_list>[-\w]+)/(?P<num>\d{1})/$', views.post_list, name='post_list'),
url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',
views.post_detail,name='post_detail'),
url(r'^(?P<post_id>\d+)/share/$', views.post_share,name='post_share'),
url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list,name='post_list_by_tag'),
url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
url(r'^edit/(?P<pk>\d+)/$', views.PostUpdate.as_view(), name="post-update"),
url(r'^profile_update/(?P<pk>\d+)/$', views.ProfileUpdate.as_view(), name="profile-update"),
url(r'^profile/(?P<my_list>[-\w]+)/$', views.profile_dispaly, name="profile_dispaly"),
url(r'^delete/(?P<pk>\d+)/$', views.DeletePost.as_view(), name="post-delete"),
url(r'^add/$', views.PostCreate.as_view(), name="post-create"),
#url(r'^add/$', views.create, name="post-create"),
]
