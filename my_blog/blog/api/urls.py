from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.PostListAPIView.as_view(), name='post_api'),
url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
url(r'^create/$', views.PostCreateAPIView.as_view(), name='create'),
url(r'^login/$', views.UserLoginAPIView.as_view(), name='login'),
url(r'^(?P<slug>[\w-]+)/$', views.PostDetailAPIView.as_view(), name='detail'),
url(r'^(?P<slug>[\w-]+)/edit/$', views.PostUpdateAPIView.as_view(), name='update'),
url(r'^(?P<slug>[\w-]+)/delete/$', views.PostDeleteAPIView.as_view(), name='delete'),
]
# urls without slug field should on the top other wise django does not know if register
#is slug or actual url as urls executed from to to down
