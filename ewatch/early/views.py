# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data

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
        # context['some_thing'] = 'Hello world'

        # -- pruebo invocacion de a_function()
        # a_function( 'Hello world 2' )

        # from ewatch.settings import BASE_DIR, API_PATH

        # print("get_context_data: BASE_DIR[%s]" % (BASE_DIR))
        # print("get_context_data: API_PATH[%s]" % (API_PATH))

        print("get_context_data: view_text[%s]" % (self.object.view_text))
        group = self.object.view_text

        # context['data'] = group_services( group )
        # show_group_services_data( context['data'] )


        _data = group_services( group )

        # ------------------------------------------------
        _host   = 0
        _cpu    = 1
        _disk   = 2
        _memory = 3
        
        hosts_list = []
        for a_list in _data:
            hosts_list.append( a_list[_host] )

        context['hosts'] = hosts_list
        # ------------------------------------------------

        return context

class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'
