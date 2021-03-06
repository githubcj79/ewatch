# -*- coding: iso-8859-15 -*-

from __future__ import unicode_literals
from __future__ import print_function


from django.shortcuts import render

# Incorporo mis utilitarios de Livestatus

# from utils.testing import a_function
from utils.group_services import group_services, show_group_services_data, show_cpu_load, show_disk, show_memory
from utils.live_utils import  HostsGroup, ServiceStateHist, HostWarningAndCriticalAlerts
# from utils.live_utils import LV_Connect, HostsGroup, ServiceStateHist, HostWarningAndCriticalAlerts, GroupsDictionary
from utils.state_class import HostState, GroupState
from utils.connection_class import Connection#, ShowSetAsOrderedList


# FROM REPORT

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template import loader

from .models import Country, View

from operator import itemgetter, attrgetter

country_prefix = None

class IndexView(generic.ListView):
    template_name = 'early/index.html'

    def get_queryset(self):
        """Return the list of countries."""
        return Country.objects.order_by('country_text')

class DetailView(generic.DetailView):
    model = Country
    template_name = 'early/detail.html'

    def get_context_data(self, **kwargs):
        global country_prefix
        context = super(DetailView, self).get_context_data(**kwargs)

        # print("DetailView: pk[%s]" % (self.kwargs['pk']))

        country_dict = {r'CHILE':r'CL_', r'ARGENTINA':r'AR_', r'PERU':r'PE_',
                        r'COLOMBIA':r'CO_', r'BRASIL':r'BR_',}

        # Se va a buscar a la base de datos el objeto del modelo
        # Country, asociado a la pk recibida.

        _pk = self.kwargs['pk']
        c = Country.objects.get(pk=_pk)
        _country = c.country_text
        # print( _country )

        # Se obtiene el prefijo asociado al pais.

        if _country in country_dict:
            country_prefix = country_dict[ _country ]
        else:
            print("views.py: class DetailView: key[%s] no existe en country_dict !!!" % (_country))
            country_prefix = None
        # print( country_prefix )

        connection = Connection() # It takes a 0m1.338s, to load it.
        # connection.show()

        group_set = set()
        if country_prefix in connection.country_dict:
            groups_dict = connection.country_dict[country_prefix].group_dict
            for groupname in groups_dict:
                group_set.add( groups_dict[groupname] )

        context['country_text'] = _country

        # OJO: Debería convertir set en lista y ordenarla y pasar a template la lista ...
        context['group_list'] = sorted(list(group_set), key=attrgetter('groupname'))

        return context


class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'


def view(request, group):
    global country_prefix

    # return HttpResponse("You're looking at group %s." % group)
    template = loader.get_template('early/view.html')

    print("get_context_data: group[%s]" % (group))

    connection = Connection() # It takes a 0m1.338s, to load it.

    host_dict = connection.country_dict[country_prefix].group_dict[group].host_dict

    hosts_list = []
    group_state = GroupState( group )
    for hostname in host_dict:
        print( host_dict[hostname].hostname )
        Host = HostState( host_dict[hostname].hostname )
        Host.check_cpu( host_dict[hostname].conn )
        Host.check_disk( host_dict[hostname].conn )
        Host.check_memory( host_dict[hostname].conn )
        Host.check_alerts( host_dict[hostname].conn )
        hosts_list.append( Host )
        group_state.check_host_state( Host.state )        

    context = {
        # 'hosts': hosts_list,
        'hosts': sorted(hosts_list, key=attrgetter('hostname')),
        'group': group_state,
    }

    return HttpResponse(template.render(context, request))
