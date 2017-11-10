# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services

# FROM REPORT

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Country, View


class IndexView(generic.ListView):
    template_name = 'early/index.html'

    def get_queryset(self):
        """Return the list of countries."""
        return Country.objects.order_by('country_text')

class DetailView(generic.DetailView):
    model = Country
    template_name = 'early/detail.html'

class ViewView(generic.DetailView):
    model = View
    template_name = 'early/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewView, self).get_context_data(**kwargs)
        context['publisher'] = self.object
        context['some_thing'] = 'Hello world'

        # -- pruebo invocacion de a_function()
        # a_function( 'Hello world 2' )

        # from ewatch.settings import BASE_DIR, API_PATH

        # print("get_context_data: BASE_DIR[%s]" % (BASE_DIR))
        # print("get_context_data: API_PATH[%s]" % (API_PATH))

        print("get_context_data: view_text[%s]" % (view.view_text))

        group_services( view.view_text )

        return context

class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'
