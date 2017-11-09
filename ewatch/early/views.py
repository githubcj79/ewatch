# Initial

#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from __future__ import unicode_literals


from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the early index.")


# ----------------------------------------------------------------
# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# # from django.shortcuts import render

# # # Create your views here.

# from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.views import generic

# from .models import Country, View

# class IndexView(generic.ListView):
#     model = Country
#     template_name = 'early/index.html'
#     # Sin embargo, para ListView, la variable contextual generada de forma automática es country_list

#     def get_queryset(self):
#         """ """
#         return Country.objects.order_by('country_text')
