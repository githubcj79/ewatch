# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data, show_cpu_load, show_disk, show_memory
from utils.live_utils import LV_Connect, HostsGroup, ServiceStateHist, HostWarningAndCriticalAlerts
from utils.state_class import HostState, GroupState

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
    # -------------------------------------------------------

    # def get_context_data(self, **kwargs):
    #     context = super(DetailView, self).get_context_data(**kwargs)
    #     print("DetailView: pk[%s]" % (self.kwargs['pk']))

    # -------------------------------------------------------

class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'


class ViewView(generic.DetailView):
    model = View
    template_name = 'early/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewView, self).get_context_data(**kwargs)

        group = self.object.view_text
        # print("get_context_data: group[%s]" % (group))

        conn = LV_Connect()
        # print("get_context_data: conn[%s]" % (conn))

        hosts_to_process = HostsGroup( conn, group )
        # print( hosts_to_process )

        hosts_list = []
        # ------------------------------------------------------------
        Group = GroupState( group )
        # ------------------------------------------------------------
        for hostname in hosts_to_process:
            print( hostname )
            Host = HostState( hostname )
            Host.check_cpu( conn )
            Host.check_disk( conn )
            Host.check_memory( conn )
            Host.check_alerts( conn )
            hosts_list.append( Host )
            # ------------------------------------------------------------
            Group.check_host_state( Host.state )
            # ------------------------------------------------------------

        context['hosts'] = hosts_list
        # ------------------------------------------------------------
        context['group'] = Group
        # ------------------------------------------------------------

        return context
