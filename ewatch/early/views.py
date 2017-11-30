# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data, show_cpu_load, show_disk, show_memory
from utils.live_utils import LV_Connect, HostsGroup, ServiceStateHist, HostWarningAndCriticalAlerts, GroupsDictionary
from utils.state_class import HostState, GroupState

# FROM REPORT

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import loader





from .models import Country, View


class IndexView(generic.ListView):
    template_name = 'early/index.html'

    def get_queryset(self):
        """Return the list of countries."""
        return Country.objects.order_by('country_text')

class DetailView(generic.DetailView):
    model = Country
    template_name = 'early/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # -------------------------------------------------------
        print("DetailView: pk[%s]" % (self.kwargs['pk']))

        country_dict = {r'CHILE':r'CL_', r'ARGENTINA':r'AR_', r'PERU':r'PE_',
                        r'COLOMBIA':r'CO_', r'BRASIL':r'BR_',}


        '''
        debo ir a buscar a la base de datos el objeto del modelo
        Country, para ver a que pais corresponde --> inferir el
        prefijo Ej: CL_

        Con eso puedo ir a buscar el diccionario de grupos
        y usando key == prefijo, obtener el set de grupos 
        asociados.

        Pregunta: vale la pena definir un "objeto" que almacene esta info ?
        '''

        # Se va a buscar a la base de datos el objeto del modelo
        # Country, asociado a la pk recibida.

        _pk = self.kwargs['pk']
        c = Country.objects.get(pk=_pk)
        _country = c.country_text
        print( _country )

        # Se obtiene el prefijo asociado al pais.

        if _country in country_dict:
            _prefix = country_dict[ _country ]
        else:
            print("views.py: class DetailView: key[%s] no existe en country_dict !!!" % (_country))
            exit( 1 )
        print( _prefix )

        conn = LV_Connect()

        # Se obtiene el diccionario de grupos
        groups_dict = GroupsDictionary( conn )

        # Se obtiene el set de grupos asociado al prefijo del pais.
        if _prefix in groups_dict:
            group_set = groups_dict[ _prefix ]
        else:
            print("views.py: class DetailView: key[%s] no existe en groups_dict !!!" % (_prefix))
            exit( 1 )
        print( group_set )

        # -------------------------------------------------------
        context['country_text'] = _country
        # -------------------------------------------------------
        '''
        OJO: Debería convertir set en lista y ordenarla y pasar a template la lista ...
        '''
        context['group_list'] = sorted(list(group_set))
        # -------------------------------------------------------
        return context



class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'


class ViewView(generic.DetailView):

    model = View
    template_name = 'early/view.html'

    def get_context_data(self, **kwargs):
        context = super(ViewView, self).get_context_data(**kwargs)

        group = self.kwargs['group']

        # group = self.object.view_text
        print("get_context_data: group[%s]" % (group))

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


# def view(request, group):
#     return HttpResponse("You're looking at group %s." % group)

def view(request, group):
    # return HttpResponse("You're looking at group %s." % group)
    template = loader.get_template('early/view.html')
    # ------------------------------------------------------------
    # group = self.kwargs['group']

    # group = self.object.view_text
    print("get_context_data: group[%s]" % (group))

    conn = LV_Connect()
    # print("get_context_data: conn[%s]" % (conn))

    hosts_to_process = HostsGroup( conn, group )
    # print( hosts_to_process )

    hosts_list = []
    Group = GroupState( group )

    for hostname in hosts_to_process:
        print( hostname )
        Host = HostState( hostname )
        Host.check_cpu( conn )
        Host.check_disk( conn )
        Host.check_memory( conn )
        Host.check_alerts( conn )
        hosts_list.append( Host )
        Group.check_host_state( Host.state )

    # ------------------------------------------------------------
    context = {
        'hosts': hosts_list,
        'group': Group,
    }
    return HttpResponse(template.render(context, request))
