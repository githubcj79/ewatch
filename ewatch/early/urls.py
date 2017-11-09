# Initial view

# from django.conf.urls import url

# from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
# ]

#-----------------------------------------------------
# Work in progress

from django.conf.urls import url

from . import views

app_name = 'early'
urlpatterns = [
    # ex: /early/
    url(r'^$', views.CountriesView.as_view(), name='countries'),
    # ex: /early/CHILE/
    url(r'^(?P<pk>[A-Z]+)/$', views.ViewView.as_view(), name='view'),
    # ex: /early/CHILE/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
]
#-----------------------------------------------------

#	From app report

# from django.conf.urls import url

# from . import views

# app_name = 'report'
# urlpatterns = [
#     # ex: /report/
#     url(r'^$', views.IndexView.as_view(), name='index'),
#     # ex: /report/5/
#     url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#     # ex: /report/5/results/
#     url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     # ex: /report/5/vote/
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]