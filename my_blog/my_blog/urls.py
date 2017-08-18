from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from taggit_templatetags2.views import TagCanvasListView
sitemaps = {
'posts': PostSitemap,
}
urlpatterns = [
url(r'^admin/', include(admin.site.urls)),
url(r'^$', views.post_list, name='postlist'),
 url(r'^accounts/logout/$', auth_views.logout, name='logout'),
 #so that logout confirmation page is NOT diplayed
url(r'^blog/', include('blog.urls',namespace='blog',app_name='blog')),
url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
url(r'^ckeditor/', include('ckeditor_uploader.urls')),
url(r'^api/blog/', include('blog.api.urls',namespace='api',app_name='api_blog')),
 url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   url(r'^accounts/', include('allauth.urls')),
    url(r'^tags/', include('taggit_templatetags2.urls')),
 url(r'^tag-list/(?P<tag_id>.*)/(?P<tag_slug>.*)/', TagCanvasListView.as_view(), name='myurlname'),
]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
