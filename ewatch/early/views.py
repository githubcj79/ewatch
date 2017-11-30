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

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        print("DetailView: pk[%s]" % (self.kwargs['pk']))

        country_dict = {r'CHILE':r'CL_', r'ARGENTINA':r'AR_', r'PERU':r'PE_',
                        r'COLOMBIA':r'CO_', r'BRASIL':r'BR_',}


        # data = {'a':1,'b':2,'c':3}
        # prefix_list = [ r'CL_', r'AR_', r'PE_', r'CO_', r'BR_', ]


        '''
        debo ir a buscar a la base de datos el objeto del modelo
        Country, para ver a que pais corresponde --> inferir el
        prefijo Ej: CL_

        Con eso puedo ir a buscar el diccionario de grupos
        y usando key == prefijo, obtener el set de grupos 
        asociados.

        Pregunta: vale la pena definir un "objeto" que almacene esta info ?
        '''

        _pk = self.kwargs['pk']
        c = Country.objects.get(pk=_pk)
        # print( c )
        _country = c.country_text
        print( _country )

        if _country in country_dict:
            _prefix = country_dict[ _country ]
        else:
            print("views.py: class DetailView: key[%s] no existe !!!" % (_country))
            exit( 1 )

        print( _prefix )

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
