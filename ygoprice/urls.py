from django.conf.urls import patterns, url

urlpatterns = patterns('ygoprice.views',
    url(r'^$', 'list', name='list'),
)