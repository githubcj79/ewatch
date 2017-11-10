
# FROM REPORT

from django.conf.urls import url

from . import views

app_name = 'early'
urlpatterns = [
    # ex: /early/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /early/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /early/view/2/
    url(r'^view/(?P<pk>[0-9]+)/$', views.ViewView.as_view(), name='view'),
]
