from django.conf.urls import url

from . import views as post_views

urlpatterns = [
    url(r'^$', post_views.PostListView.as_view(), name='postlist'),
    url(r'^create/$', post_views.postCreateView, name='postcreate'),
    url(r'^(?P<slug>[\w-]+)/$', post_views.PostDetailView.as_view(), name='postdetail'),    
    url(r'^(?P<slug>[\w-]+)/edit/$', post_views.PostUpdateView.as_view(), name='postedit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_views.PostDeleteView.as_view(), name='postdelete'),
    
]
