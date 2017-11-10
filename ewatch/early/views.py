# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

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

# ----------------------------------------
class ViewView(generic.DetailView):
    model = View
    template_name = 'early/view.html'
# ----------------------------------------

class ResultsView(generic.DetailView):
    model = Country
    template_name = 'early/results.html'
