# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data, show_cpu_load, show_disk, show_memory
from utils.live_utils import LV_Connect, HostsGroup, ServiceStateHist, HostWarningAndCriticalAlerts

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

        # print("get_context_data: view_text[%s]" % (self.object.view_text))
        group = self.object.view_text

        _host   = 0
        _cpu    = 1
        _disk   = 2
        _memory = 3

        hosts_list = []
        cpu_list = []
        disk_list = []
        memory_list = []
        alerts_list = []
        
        conn = LV_Connect()
        # print("get_context_data: conn[%s]" % (conn))

        hosts_to_process = HostsGroup( conn, group )
        # print( hosts_to_process )

        service_description_list = ['CPU load', 'Disk IO SUMMARY', 'Memory']

        for host in hosts_to_process:
            # print( host )
            hosts_list.append( host )

            '''
            i = _cpu - 1
            for desc in service_description_list:
                a_list = ServiceStateHist( conn, host, desc )
                # print( a_list )

                if len(a_list):
                    a_list = a_list[0]
                    # print( a_list )
                    a_str = "%s %.1f%% OK %.1f%% WARNING %.1f%% CRITICAL" % (desc, 100 * float(a_list[-3]), 100 * float(a_list[-2]), 100 * float(a_list[-1]))
                    # print( a_str )
                    if _cpu == i + 1:
                        cpu_list.append( a_str )
                    if _disk == i + 1:
                        disk_list.append( a_str )
                    if _memory == i + 1:
                        memory_list.append( a_str )
                    i += 1
                    i %= _memory
            '''

            # ----------------solo para probar----------------
            a_str = 'Solo para testing'
            cpu_list.append( a_str )
            disk_list.append( a_str )
            memory_list.append( a_str )
            # ------------------------------------------------
        
            new_alert_list = []
            alerts_to_process = HostWarningAndCriticalAlerts( conn, host )
            for alert in alerts_to_process:
                alert_str = ' '.join( map( str,alert ) )
                # print( alert_str )
                new_alert_list.append( alert_str )

            alerts_list.append( new_alert_list )

        # ------------------------------------------------

        context['hosts'] = hosts_list
        context['cpus'] = cpu_list
        context['disks'] = disk_list
        context['memories'] = memory_list
        context['alerts'] = alerts_list

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
