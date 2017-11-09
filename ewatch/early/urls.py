# FROM REPORT

from django.conf.urls import url

from . import views

app_name = 'early'
urlpatterns = [
    # ex: /early/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /early/5/
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /early/5/results/
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /early/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

# ORIGINAL

# from django.conf.urls import url

# from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
# ]