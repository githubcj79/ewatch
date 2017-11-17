# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data, show_cpu_load, show_disk, show_memory
from utils.live_utils import LV_Connect, HostsGroup, ServiceStateHist

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

        print("get_context_data: view_text[%s]" % (self.object.view_text))
        group = self.object.view_text

        # ------------------------------------------------
        conn = LV_Connect()
        print("get_context_data: conn[%s]" % (conn))

        hosts_list = HostsGroup( conn, group )
        print( hosts_list )

        service_description_list = ['CPU load', 'Memory', 'Disk IO SUMMARY']

        for host in hosts_list:
            # print( host )

            for desc in service_description_list:
                a_list = ServiceStateHist( conn, host, desc )
                print( a_list )
                return # solo para no hacer tan larga la iteracion

        #         if len(a_list):
        #             a_list = ServiceStateHist( conn, host, desc )[0]
        #             print a_list
        #             print "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))

            # alert_list = HostCriticalAlerts( conn, host )
            # for alert in alert_list:
            #     print alert


        # ------------------------------------------------


        return context

class ViewView_old_version(generic.DetailView):
    model = View
    template_name = 'early/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewView, self).get_context_data(**kwargs)
        context['publisher'] = self.object

        print("get_context_data: view_text[%s]" % (self.object.view_text))
        group = self.object.view_text

        _data = group_services( group )

        # ------------------------------------------------
        _host   = 0
        _cpu    = 1
        _disk   = 2
        _memory = 3

        hosts_list = []
        cpu_list = []
        disk_list = []
        memory_list = []
        
        for a_list in _data:
            hosts_list.append( a_list[_host] )
            cpu_list.append( show_cpu_load( a_list[_cpu] ) )
            disk_list.append( show_disk( a_list[_disk] ) )
            memory_list.append( show_memory( a_list[_memory] ) )

        context['hosts'] = hosts_list
        context['cpus'] = cpu_list
        context['disks'] = disk_list
        context['memories'] = memory_list
        # ------------------------------------------------

        return context

class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'
